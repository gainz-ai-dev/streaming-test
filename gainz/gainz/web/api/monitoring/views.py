from fastapi import APIRouter

# Basically, these API only for testing. Not using in production. But reserved for developers reference. 

views = APIRouter()

@views.get("/health")
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """

@views.get("/test")
def test():
    return {"Hello": "World"}

@views.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


