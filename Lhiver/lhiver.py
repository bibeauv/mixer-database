import time
from itertools import takewhile
from pathlib import Path
from typing import List, Dict, Iterable
import getpass
import configparser
import pyslurm

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
SUBMIT_DELAY_MS = float(CONFIG['lhiver']['submission_delay_ms']) / 1000

USERNAME = getpass.getuser()
BASE_JOB_PARAMS = {  # TODO
    'ntasks': 1
}


def get_working_directories() -> List[Path]:
    """
    Returns a list of paths where jobs will be submitted
    :return: A list of paths
    """
    # TODO walk directories
    return [Path().absolute()]


def get_queued_jobs_ids() -> List[int]:
    user_jobs = pyslurm.job().find_user(USERNAME).items()
    return [job[0]
            for job in user_jobs
            if job[1]['job_state'] in {'PENDING', 'RUNNING'}
            and job[1]['name'] != CONFIG['self_job']['job_name']]  # TODO add more conditions


def is_submitted(directory: Path) -> bool:
    """
    Checks if the given directory was associated with a submitted job
    :param directory: The directory to check
    :return: True if a job was successfully submitted with the given directory
    """
    # TODO Check .out files and/or user jobs
    return False
# TODO Rework required params


def create_job_params(directory: Path) -> Dict[str, str]:
    """
    Submits a job to Slurm.
    :param directory: The working directory of the job
    :return: The ID of the submitted job
    """
    # TODO params
    # TODO Tags?
    job_params = dict(BASE_JOB_PARAMS)
    job_params.update({
        'job_name': 'inline_sleep_job',
        'time': '60:00',
        'mem_per_cpu': 100,
        'wrap': 'srun sleep 60'
    })

    return job_params


def submit_self(dependencies: Iterable[int]) -> int:
    """
    Submits this very script to Slurm.
    The created job will only be queued for execution (PENDING state) if any of its dependencies have terminated.
    :param dependencies: The job IDs of the jobs to depend on
    :return: The ID of the submitted job
    """
    current_file_path = Path(__file__).absolute()
    dependencies_str = 'afterany:{}'.format('?afterany:'.join(map(str, dependencies)))

    self_job_params = dict(BASE_JOB_PARAMS)
    self_job_params.update({
        'job_name': CONFIG['self_job']['job_name'],
        'ntasks': 1,
        'time': CONFIG['self_job']['job_name'],
        'mem_per_cpu': CONFIG['self_job']['mem_per_cpu'],
        'dependency': dependencies_str,
        'wrap': 'srun {} {}'.format(CONFIG['self_job']['python_interpreter'], str(current_file_path))
    })

    return submit_job(self_job_params)


def submit_job(params: Dict[str, str]) -> int:
    time.sleep(SUBMIT_DELAY_MS)
    return pyslurm.job().submit_batch_job(params)


if __name__ == '__main__':
    # 0. Config/params
    # 1. List directories
    # 2. Check if submitted
    # 3. Format job params
    # 4. Submit job
    # 5. Queue self with dependencies

    directories = get_working_directories()

    queued_jobs_ids = get_queued_jobs_ids()
    job_ids = set(queued_jobs_ids)
    jobs_to_submit_count = int(CONFIG['lhiver']['max_jobs']) - len(queued_jobs_ids)

    for working_directory in takewhile(lambda _: len(job_ids) < jobs_to_submit_count, directories):
        if is_submitted(working_directory):
            continue

        current_job_params = create_job_params(working_directory)  # TODO
        submitted_job_id = submit_job(current_job_params)
        job_ids.add(submitted_job_id)

    submit_self(job_ids)
