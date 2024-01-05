import subprocess
from pydantic import BaseModel
import flamethrower.config.constants as config
from flamethrower.models.llm import LLM
from flamethrower.context.conv_manager import ConversationManager
from flamethrower.agents.file_writer import FileWriter
from flamethrower.utils.token_counter import TokenCounter
from flamethrower.utils.diff import Diff
from flamethrower.shell.printer import Printer

json_schema = {
    'type': 'object',
    'properties': {
        'actions': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'action': {
                        'type': 'string',
                        'enum': ['run', 'write', 'completed']
                    },
                    'command': { 'type': 'string' },
                    'file_paths': { 'type': 'string' }
                },
                'required': ['action'],
                'allOf': [
                    {
                        'if': { 'properties': { 'action': { 'const': 'run' } } },
                        'then': { 'required': ['command'] }
                    },
                    {
                        'if': { 'properties': { 'action': { 'const': 'write' } } },
                        'then': { 'required': ['file_paths'] }
                    }
                ]
            }
        },
    },
    'required': ['actions']
}

system_message = f"""
You are an extremely powerful programming assistant that lives inside the unix terminal.
You have a single, crucial task: to categorize LLM responses into a list of 3 possible actions:
  1. Run a command on the terminal and observe its output
  2. Rewrite code in a given target file
  3. Indicate that your job has been completed. **If so, don't recommend other tests or suggestions.**
Sometimes you need to perform multiple actions, so explicitly mention that. For example, if one action is writing to a file,
then make sure to test it using the run script or command, which was likely given in the stdout logs.
Once you tested the new code and realized you got a positive output, indicate your job is completed.
It is crucial that you return a JSON object with the following JSON Schema:
    {json_schema}
"""

class Executor(BaseModel):
    max_retries: int = 4
    nl_llm: LLM = None
    json_llm: LLM = None
    json_schema: dict = json_schema
    conv_manager: ConversationManager = None
    file_writer: FileWriter = None
    token_counter: TokenCounter = None
    printer: Printer = None

    def __init__(self, **data):
        super().__init__(**data)
        self.nl_llm = LLM(
            token_counter=self.token_counter
        )
        self.json_llm = LLM(
            system_message=system_message,
            token_counter=self.token_counter
        )
        self.file_writer = FileWriter(
            token_counter=self.token_counter
        )

    def execute_action(self, command: str) -> str:
        output = ''
        try:
            completed_process = subprocess.run(
                command, 
                shell=True,
                check=True,
                text=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT
            )
            output = completed_process.stdout
        except subprocess.CalledProcessError as e:
            output = f'Error: {e.output}'

        return output
    
    def new_implementation_run(self, query: str, conv: list) -> None:
        """
        To complete a debugging run, we need:
          1. An objective
          2. A starting point
          3. A series of steps to complete the objective
        """

        # Initial understanding of the problem and generation of solution
        stream = self.nl_llm.new_streaming_chat_request(messages=conv)
        self.printer.print_llm_response(stream)
        
        action = ''
        for _ in range(self.max_retries):
            last_driver_res = self.get_last_assistant_response()
            decision = self.make_decision_from(query, last_driver_res)
            
            actions: list = decision['actions']
            for obj in actions:
                action = obj['action']
                
                if action == 'run':
                    command = obj['command']
                    self.printer.print_regular(command)
                    output = self.execute_action(command)
                    self.printer.print_regular(output)
                    self.conv_manager.append_conv(
                        role='user',
                        content=command,
                        name='human',
                    )
                    self.conv_manager.append_conv(
                        role='user',
                        content=output,
                        name='stdout',
                    )
                
                elif action == 'write':
                    file_paths = obj['file_paths']
                    self.file_writer.write_code(file_paths, last_driver_res)
                    self.conv_manager.append_conv(
                        role='user',
                        content=f'Done with updating file: `{file_paths}`.',
                        name='human',
                    )
                    self.printer.print_green(f'Successfully updated {file_paths}\n', reset=True)
                
                elif action == 'completed':
                    diffs = Diff(printer=self.printer).get_diffs()
                    # TODO: diffs for just that 1 file?
                    # self.printer.print_diffs(diffs)
                    return
                
                else:
                    raise Exception('Invalid action')

            # Subsequent implementations of the solution
            conv = self.conv_manager.get_conv()
            stream = self.nl_llm.new_streaming_chat_request(messages=conv)
            self.printer.print_llm_response(stream)
        
        # Max retries exceeded
        self.printer.print_red("\nToo many iterations, I'm going to need your help to debug this.", reset=True)

    def make_decision_from(self, objective: str, latest_response: str) -> dict:
        query = (
            f'This is the objective:\n{objective}'
            f'This is the latest response:\n{latest_response}'
            'Given this objective and response, choose a possible action.'
        )
        self.printer.print_default('\n')
        decision = self.json_llm.new_json_request(
            query=query,
            json_schema=self.json_schema,
            loading_message='🤖 Determining next step...'
        )

        return decision
    
    def get_last_assistant_response(self) -> str:
        with open(config.get_last_response_path(), 'r') as f:
            return f.read()
    