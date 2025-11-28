from models.user_model import  User

class TestModel:
    def test_user_model(self):
        assert "username" in User.__table__.columns
        assert "password" in User.__table__.columns

        username_col = User.__table__.columns["username"]
        password_col = User.__table__.columns["password"]

        assert username_col.unique
        assert not username_col.nullable
        assert not password_col.nullable

        assert username_col.type.__class__.__name__ == "String"
        assert password_col.type.__class__.__name__ == "String"