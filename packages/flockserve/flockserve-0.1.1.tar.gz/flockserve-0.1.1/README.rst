==========
flockserve
==========


.. image:: https://img.shields.io/pypi/v/flockserve.svg
        :target: https://pypi.python.org/pypi/flockserve

.. image:: https://img.shields.io/travis/anil-gurbuz/flockserve.svg
        :target: https://travis-ci.com/jdooodle/flockserve

.. image:: https://readthedocs.org/projects/flockserve/badge/?version=latest
        :target: https://flockserve.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/anil-gurbuz/flockserve/shield.svg
     :target: https://pyup.io/repos/github/jdooodle/flockserve
     :alt: Updates



Open-source Sky Computing Inference Endpoint
============================================

Overview
--------

Flockserve is an Open-source Inference Endpoint that provides a scalable and efficient solution for deploying machine learning models in a distributed and cloud-native environment. This inference endpoint is designed to seamlessly integrate with `skypilot <https://skypilot.readthedocs.io>`_ infrastructure, allowing for dynamic resource allocation and optimal model serving.

Features
--------

- **Scalability:** Easily scale your inference endpoint based on the demand using cloud resources.

- **Skypilot Integration:** Leverage the power of skypilot for dynamic and distributed computing.

- **Flexible Model Support:** Support for a variety of machine learning frameworks and model formats as they are run through skypilot engine.

- **RESTful API:** Simple and intuitive API for interacting with the inference endpoint.

- **Monitoring and Logging:** Monitor the performance and logs of deployed models for effective debugging and optimization.

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

- Python >= 3.7  <= 3.10
- Docker (if using containerized deployment)

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install flockserve

Usage
~~~~~

1. Import the `flockserve` library in your project.

.. code-block:: python

   from flockserve import *

2. Set configurations and initialize the inference endpoint and run the skypilot job.

.. code-block:: python

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




Configuration
-------------

You can configure the inference endpoint as shown in the above sample. Also, to configure skypilot job, you would need a  YAML configuration file as usual in skypilot.


Contributing
------------

We welcome contributions from the community. If you'd like to contribute, please follow our `Contribution Guidelines <CONTRIBUTING.md>`_.


Acknowledgments
---------------

- Special thanks to contributors and the open-source community.

Support
-------

For any issues or questions, please `create an issue <https://github.com/jdooodle/flockserve/issues>`_.


* Free software: Apache Software License 2.0


TODO
----

- [ ] Add support for other cloud providers
- [ ] Add documentation for usage
