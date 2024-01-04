# Mara Cron

Mini package for managing cron jobs via mara.

&nbsp;

## Installation

To use the library directly:

```
pip install mara-cron
```

&nbsp;

## Config of cron jobs

To configure cron jobs in mara you just need to add a new function `MARA_CRON_JOBS`
in your module or app in the `__init__.py` file.

Here is a sample which has two jobs:
1. the job `cleanup_data_folder` clears all data from the local folder `/data/`. This job is by default disabled.
2. the job `nightly` runs the root pipeline at 01:00 o'clock each day

_Note:_ The MaraJob job requires that you define the `PATH` environment variable in your crontab. Cron by default uses just `/usr/bin:/bin` which is not enough. I recommend using the distribution default e.g. `/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`.

```python
def MARA_CRON_JOBS():
    from mara_cron.job import CronJob, MaraJob
    return [
        CronJob(id='cleanup_data_folder',
                description='Clean up the data folder',
                default_time_pattern='0 0 * * *',
                command='rm -rf /data/*',
                enabled=False),
        MaraJob(id='nightly',
                description="Nightly run of the BI system",
                default_time_pattern='0 1 * * *',
                command='pipelines run'),
    ]
```

## Local config

Sample local config to activate crontab management in your mara app:

```python
from mara_app.monkey_patch import patch
import mara_cron.config

# Activates mara_cron jobs. If not set all jobs are
# by default disabled and can only be activated via
# executing:
#    mara cron enable --job-id "my_job_id"
patch(mara_cron.config.enabled)(lambda: True)

# Optional parameter to specify a mara instance name
# This is necessary to separate multiple environments running
# on the same user
patch(mara_cron.config.instance_name)(lambda: 'prod')
```

## CLI

This package contains the following cli commands (`mara cron <command>`):

| Command        | Description
| -------------- | --------------
| `enable --job-id "my_job_id" [--module "module_name"]` | Enables a specific job regardless of the configuration.
| `disable --job-id "my_job_id" [--module "module_name"]` | Disables a specific job.
| `schedule-job --job-id "my_job_id"` | Schedules a job to run in less than 1 minute.
| `list-crontab` | Lists the current cron tab settings
| `list-crontab --with-changes` | Lists the current cron tab including the changes not yet written
| `write-crontab` | Writes all not published changes to the crontab
| `clear-crontab` | Removes all mara jobs from the crontab. *Note* This applies to all instances !!!
