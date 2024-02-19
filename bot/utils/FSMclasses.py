from aiogram.fsm.state import StatesGroup, State



class AddService(StatesGroup):
    category_id: str = State()
    name: str = State()
    description: str = State()
    photo: str = State()

class AddCategory(StatesGroup):
    name: str = State()


class AskQuestion(StatesGroup):
    text: str = State()


class ChangeMessage(StatesGroup):
    text: str = State()
    photo: str = State()