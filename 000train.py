
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# # @app.get("/")
# # def get_home():
# #     return FileResponse("templates/home.html")

# @app.get("/items/admin")
# def get_admin():
#     return "HI ADMIN"

# @app.get("/items/{item_id}")
# def get_item(item_id: int, q:Union[str, None] = None):
#     return {"item_id": item_id, "q":q}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"Item price":item.price, "item id":item_id}

# @app.get("/{word1}-{word2}-{word3}")
# def get_words(word1: str, word2: str, word3: str):
#     return{"word1": word1, "word2": word2, "word3": word3}

# @app.get("/min-max/{name}")
# def get_minmax(name: str = Path(min_length=3, max_length=5)):
#     return {"name":name}

# @app.get("/phone/{phone}")
# def get_phone(phone: str = Path(pattern=r"^\d{11}$")):
#     return {"phone":phone}

# @app.get("/users/{name}")
# def get_users(name = Path(min_length=3, max_length=10), age: int = 15,  height: int = Query(default=170, ge=50, lt=250)):
#     return {"name": name, "age": age, "height": height}

# @app.get("/hobbies")
# def get_hobby(hobby: list[str] = Query()):
#     return { "hobby": hobby}

# @app.get("/old", response_class= RedirectResponse)
# def old():
#     return "/"

# @app.get("/telegram", response_class= RedirectResponse)
# def telega():
#     return RedirectResponse("https://web.telegram.org")

# #app.mount("/", StaticFiles(directory="templates", html=True))

# @app.post("/hello")
# def get_hello(name: str = Body(embed=True), age: int = Body(embed=True)):
#     return {"message": f"{name}, your age is {age}"}

from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    descr: Union[str, None] = None


@app.post("/")
async def get_item(item: Item):
    return f"With id {item.id} we have {item.name} with descr {item.descr}"

