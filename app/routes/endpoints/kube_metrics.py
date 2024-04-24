from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/kube-metrics")


@router.get("/namespaces", status_code=status.HTTP_200_OK)
def get_namespaces():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_mocked_namespaces()
    return JSONResponse({"namespaces": response})


@router.get("/nodes", status_code=status.HTTP_200_OK)
def get_nodes():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_mocked_nodes()
    return JSONResponse({"nodes": response})


@router.get("/pods", status_code=status.HTTP_200_OK)
def get_pods():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_mocked_nodes()
    return JSONResponse({"pods": response})


@router.get("/deployments", status_code=status.HTTP_200_OK)
def get_deployments():
    from app.entrypoint import app

    response = app.kube_metrics_service.get_mocked_deployments()
    return JSONResponse({"deployments": response})
