Dyff Design Overview
====================

The Dyff Platform consists of two major components:

    ``dyff-operator``
        A Kubernetes `operator <https://kubernetes.io/docs/concepts/extend-kubernetes/operator/>`_ that manages a set of `custom resources <https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/>`_ . The Dyff Operator launches "workflows" composed of one or more "workflow steps" in response to creation of Dyff k8s resources.

    ``dyff-api``
        A full-featured cloud platform and Web API built around the Dyff Operator functionality. The Dyff API components include an API server, message broker, database, and various internal services that coordinate platform operations. An ``orchestrator`` service creates and manages Dyff k8s resources via the k8s API in response to Dyff API actions, and the Dyff Operator in turn does the actual work in response to these k8s resources.

.. image:: dyff-service-diagram.svg
