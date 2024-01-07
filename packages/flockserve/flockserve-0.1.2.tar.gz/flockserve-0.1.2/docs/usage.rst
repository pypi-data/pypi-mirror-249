=====
Usage
=====

To use flockserve in a project::

    import flockserve
    configurations = {
    "WORKER_CAPACITY": 30, # Number of requests that can be handled concurrently by a single worker
    "WORKER_NAME_PREFIX": "qa-llm-server",
    "SKYPILOT_JOB_FILE": "path_to_skypilot_job.yaml",
    "SKYPILOT_SERVIC_ACC_KEYFILE": "path_to_cloud_auth_keyfile",
    "INFRA": "SKYPILOT",
    "HOST": "0.0.0.0", # Accept connections from anywhere
    "PORT": 8000, # Port to listen on
    }

    conf = Config(**configurations)
    app = Flockserve_app(conf)
    app.run()
