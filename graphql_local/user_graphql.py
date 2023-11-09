import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from db.models.user import User as UserDB
from db.models.address import Address as AddressDB
from model import UserInput
from orm import insert_user


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserDB
        # use `only_fields` to only expose specific fields ie "name"
        # only_fields = ("name",)
        # use `exclude_fields` to exclude specific fields ie "last_name"
        # exclude_fields = ("last_name",)


class Address(SQLAlchemyObjectType):
    class Meta:
        model = AddressDB


class Query(graphene.ObjectType):
    user = graphene.Field(
        User, 
        id=graphene.ID(required=True),
        required=True
    )
    users = graphene.List(User)

    def resolve_user(root, info, id):
        return User.get_node(info, id)

    def resolve_users(self, info):
        query = User.get_query(info)  # SQLAlchemy query
        return query.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int(required=True)
        is_alive = graphene.Boolean(default_value=True)
        last_name = graphene.String(required=True)
        height = graphene.Float(required=True)
        weigth = graphene.Int(required=True)
        fullname = graphene.String()
        # addresses = graphene.List(Address)

    id: int = graphene.Int()
    name: str = graphene.String()
    age: int = graphene.Int()
    is_alive: bool = graphene.Boolean()
    last_name: str = graphene.String()

    def mutate(root, info, name, age, is_alive, last_name, height, weigth, fullname = None, addresses = None):
        # if isinstance(addresses, list) and len(addresses) == 0:
        #     addresses = None

        new_user = UserInput(
            name=name,
            last_name=last_name,
            age=age,
            is_alive=is_alive,
            height=height,
            weigth=weigth,
            full_name=fullname,
            addresses=addresses
        )

        print(info.context["session"])
        return insert_user(new_user, info.context["session"])
    

class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema_user = graphene.Schema(query=Query, mutation=UserMutation)