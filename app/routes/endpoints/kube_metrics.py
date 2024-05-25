from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/kube-metrics")


@router.get("/namespaces", status_code=status.HTTP_200_OK)
def get_namespaces():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_namespaces()
    return JSONResponse({"namespaces": response})


@router.get("/nodes", status_code=status.HTTP_200_OK)
def get_nodes():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_nodes()
    return JSONResponse({"nodes": response})


@router.get("/pods", status_code=status.HTTP_200_OK)
def get_pods():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_pods()
    return JSONResponse({"pods": response})


@router.get("/deployments", status_code=status.HTTP_200_OK)
def get_deployments():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_deployments()
    return JSONResponse({"deployments": response})


@router.get("/node-metrics", status_code=status.HTTP_200_OK)
def get_nodes_metrics():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_node_metrics_from_db()
    return JSONResponse({"node-metrics": response})


@router.get("/pod-metrics", status_code=status.HTTP_200_OK)
def get_pods_metrics():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_pod_metrics_from_db()
    return JSONResponse({"pod-metrics": response})


@router.get("/container-metrics/{name}", status_code=status.HTTP_200_OK)
def get_container_metrics(name: str):
    from app.entrypoint import app

    response = app.kube_metrics_service.get_container_metrics_from_db(name)
    return JSONResponse(response)


@router.get("/pod-limits/{pod_name}", status_code=status.HTTP_200_OK)
def get_container_metrics(pod_name: str):
    from app.entrypoint import app

    response = app.kube_metrics_service.get_pod_limits(pod_name)
    return JSONResponse({"success": "true"})