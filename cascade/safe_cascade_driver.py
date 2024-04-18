import logging
from cascade.thinker_model import ThinkerModel
from cascade.builder_model import BuilderModel
from cascade.constructor_model import ConstructorModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SafeCascadeDriver:
    def __init__(self, thinker_model, builder_model, constructor_model, max_retry_times = 4):
        self.thinker = ThinkerModel(thinker_model)
        self.builder = BuilderModel(builder_model)
        self.constructor = ConstructorModel(constructor_model)
        self.thinker_output = ""
        self.builder_output = ""
        self.constructor_output = ""
        self.max_retry_times = max_retry_times

    def execute(self, initial_input):
        logging.info("Starting the Safe Cascade process...")
        attempt_tracker = {'thinker': 0, 'builder': 0, 'constructor': 0}

        while attempt_tracker['thinker'] < self.max_retry_times:
            logging.info(f"Running Thinker, attempt {attempt_tracker['thinker'] + 1}/{self.max_retry_times}")
            self.thinker_output = self.thinker.execute(initial_input)
            if self.thinker_output is None:
                attempt_tracker['thinker'] += 1
                logging.error("Thinker model failed, retrying...")
                continue

            while attempt_tracker['builder'] < self.max_retry_times:
                logging.info(f"Running Builder, attempt {attempt_tracker['builder'] + 1}/{self.max_retry_times}")
                self.builder_output = self.builder.execute(goal=initial_input, thinker_output=self.thinker_output,max_retry_times=self.max_retry_times)
                if self.builder_output is None:
                    attempt_tracker['builder'] += 1
                    logging.error("Builder model failed, retrying...")
                    if attempt_tracker['builder'] >= self.max_retry_times:
                        logging.error("Builder model failed after maximum retries, rerunning Thinker.")
                        attempt_tracker['thinker'] += 1
                        break  # Exit builder loop, triggers rerun of thinker
                    continue

                while attempt_tracker['constructor'] < self.max_retry_times:
                    logging.info(f"Running Constructor, attempt {attempt_tracker['constructor'] + 1}/{self.max_retry_times}")
                    self.constructor_output = self.constructor.execute(goal=initial_input + self.thinker_output, builder_output=self.builder_output,max_retry_times=self.max_retry_times)
                    if self.constructor_output is None:
                        attempt_tracker['constructor'] += 1
                        logging.error("Constructor model failed, retrying...")
                        if attempt_tracker['constructor'] >= self.max_retry_times:
                            logging.error("Constructor model failed after maximum retries, rerunning Builder.")
                            attempt_tracker['builder'] += 1
                            break  # Exit constructor loop, triggers rerun of builder
                        continue

                    logging.info("Process completed successfully.")
                    return self.constructor_output

                # If constructor loop breaks because of max retries, reset constructor attempts for next builder iteration
                attempt_tracker['constructor'] = 0
            # If builder loop breaks because of thinker rerun, reset builder and constructor attempts
            attempt_tracker['builder'] = 0
            attempt_tracker['constructor'] = 0

        logging.error("Failed after maximum retries at all levels.")
        return None

# Example usage:
if __name__ == '__main__':
    driver = SafeCascadeDriver("gpt-3.5-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo",2)
    instructor_input = ("Instructor: load the material in the file I saved at ./shared/content.txt. I will listen to "
                        "its summarization while eating breakfast you don't need an output component leave the final "
                        "result in the final component is enough")
    driver.execute(instructor_input)
    print("\n\n\n*******************************************************************************\n\n")
    print(f"Final Thinker Output: {driver.thinker_output}")
    print(f"Final Builder Output: {driver.thinker_output}")
    print(f"Final Constructor Output: {driver.constructor_output}")
