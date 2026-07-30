from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import os
import logging
from typing import Optional

from front_end.config import LOGGER
import front_end.config as config


# Set logging level based on environment
if os.getenv("APP_ENV", "production") == "development":
    LOGGER.info("Running in development mode. Setting variables for development.")
    LOGGER.setLevel(logging.DEBUG)
else:
    # clear log-file
    with open("back_end/back_end.log", 'w'):
        pass
    LOGGER.info("Running in production mode. Setting variables for production.")
    LOGGER.setLevel(logging.INFO)

# Initialize FastAPI app
front_end = FastAPI(debug=(os.getenv("APP_ENV", "production")=="development"))
front_end.mount("/static", StaticFiles(directory="front_end/static"), name="static")
# Initialize Jinja2 templates
templates = Jinja2Templates(directory="front_end/templates")

# --------------------------------- #
#         Helper functions          #
# --------------------------------- #
def retrieve_cookies(request: Request) -> dict | None:
    """
    Helper function to retrieve cookies from the request.

    Args:
        request (Request): The incoming HTTP request.
    Returns:
        dict | None: A dictionary containing the cookies from the request or None.
    """
    res = {}

    res["username"] = request.cookies.get("username")
    if not res["username"] or res["username"] not in config.USERS:
        return None
    
    res["role"] = request.cookies.get("role")
    
    return res

# --------------------------------- #
#        Root page handeling        #
# --------------------------------- #
@front_end.get("/", response_class=HTMLResponse)
async def serve_root(request: Request):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register", status_code=303)
    
    username = retrieved_cookies["username"]
    role = retrieved_cookies["role"]
    response = templates.TemplateResponse("index.html", {"request": request, "username": username})
    if role:
        response.delete_cookie(key="role")
    
    return response

# --------------------------------- #
#      Registration handeling       #
# --------------------------------- #

@front_end.get("/register", response_class=HTMLResponse)
async def serve_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@front_end.post("/register_new-user")
async def handle_register(username: str = Form(...)):
    config.USERS.add(username)
    config.LOGGER.info(f"New user registered: {username}, current users: {config.USERS}")

    # Redirect to the root page and set the username cookie
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="username", value=username)
    
    return response

# --------------------------------- #
#         Logout handeling          #
# --------------------------------- #
@front_end.get("/logout", response_class=HTMLResponse)
async def serve_logout(request: Request):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    config.USERS.discard(retrieved_cookies["username"])
    config.LOGGER.info(f"User logged out: {retrieved_cookies['username']}, current users: {config.USERS if len(config.USERS) > 0 else 'No users'}")

    response = RedirectResponse(url="/register", status_code=303)
    response.delete_cookie(key="username")
    response.delete_cookie(key="role")

    return response


# --------------------------------- #
#       Waiter page handeling       #
# --------------------------------- #
@front_end.get("/waiter_home", response_class=HTMLResponse)
async def serve_waiter_home(request: Request):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    response = templates.TemplateResponse("waiter_home.html", {"request": request, "username": username, "role": "waiter"})
    response.set_cookie(key="role", value="waiter")
    return response


# --------------------------------- #
#       Kitchen page handeling      #
# --------------------------------- #
@front_end.get("/kitchen_home", response_class=HTMLResponse)
async def serve_kitchen_home(request: Request):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    response = templates.TemplateResponse("kitchen_home.html", {"request": request, "username": username, "role": "kitchen"})
    response.set_cookie(key="role", value="kitchen")
    return response

# --------------------------------- #
#         Bar page handeling        #
# --------------------------------- #
@front_end.get("/bar_home", response_class=HTMLResponse)
async def serve_bar_home(request: Request):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    response = templates.TemplateResponse("bar_home.html", {"request": request, "username": username, "role": "bar"})
    response.set_cookie(key="role", value="bar")
    return response

# --------------------------------- #
#       Dessert page handeling      #
# --------------------------------- #
@front_end.get("/dessert_home", response_class=HTMLResponse)
async def serve_dessert_home(request: Request):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    response = templates.TemplateResponse("dessert_home.html", {"request": request, "username": username, "role": "dessert"})
    response.set_cookie(key="role", value="dessert")
    return response

# --------------------------------- #
#      Checkout page handeling      #
# --------------------------------- #
@front_end.get("/checkout_home", response_class=HTMLResponse)
async def serve_checkout_home(request: Request):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    response = templates.TemplateResponse("checkout_home.html", {"request": request, "username": username, "role": "checkout"})
    response.set_cookie(key="role", value="checkout")
    return response

# --------------------------------- #
#       Order page handeling        #
# --------------------------------- #
@front_end.get("/order_edit", response_class=HTMLResponse)
async def serve_order_edit(request: Request, order_id: int):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    role = retrieved_cookies["role"]
    return templates.TemplateResponse("order_edit.html", {"request": request, "username": username, "role": role, "order_id": order_id})

@front_end.get("/order_choose-from-same-table-reference", response_class=HTMLResponse)
async def serve_order_choose_from_same_table_reference(request: Request, table_reference: str):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    role = retrieved_cookies["role"]
    return templates.TemplateResponse("order_choose_from_same_table_reference.html", {"request": request, "username": username, "role": role, "table_reference": table_reference})

@front_end.get("/choose_from_destination", response_class=HTMLResponse)
async def serve_choose_destination(request: Request, order_id: int):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    role = retrieved_cookies["role"]
    return templates.TemplateResponse("choose_from_destination.html", {"request": request, "username": username, "role": role, "order_id": order_id})

# --------------------------------- #
#       Ticket page handeling       #
# --------------------------------- #
@front_end.get("/ticket_edit", response_class=HTMLResponse)
async def serve_ticket_edit(request: Request, order_id: int, destination: str, ticket_id: Optional[int] = None):
    retrieved_cookies = retrieve_cookies(request)
    if not retrieved_cookies:
        return RedirectResponse(url="/register")
    
    username = retrieved_cookies["username"]
    role = retrieved_cookies["role"]
    return templates.TemplateResponse("ticket_edit.html", {"request": request, "username": username, "role": role, "order_id": order_id, "ticket_id": ticket_id, "destination": destination})