import requests, json

## TEST LISTAR USUARIOS ##
def test_listar_usuarios_200():
    #ARRANGE: preparar datos o entorno
    url = "http://localhost:5001/account/"

    #ACT: ejecuta la accion
    result = requests.get(url)
    response = result.json()
    status = result.status_code

    #ASSERT: validaciones
    assert status == 200, "Error al listar Usuarios"

    assert "Listado de Usuarios" in response, "Error Falta el vector de usuarios"

    if response["Listado de Usuarios"]:
        usuario = response["Listado de Usuarios"][0]
        assert "name" in usuario, "Error 'name' no existe"
        assert "username" in usuario , "Error 'username' no existe"
        assert "dni" in usuario, "Error 'dni' no existe"
        assert "phone" in usuario, "Error phone no existe"
        assert "about_me" in usuario, "Error 'about_me' no existe"
        assert "gender" in usuario, "Error no 'gender' no existe"
        assert "is_active" in usuario, "Error 'is_active' no existe"
        assert "elo" in usuario, "Error 'elo' no existe"
    assert "_links" in response , "Error falta la lista de '_links'"
    if response["_links"]:
        paginado = response["_links"]
        assert "_first" in paginado, "Error en '_first' pagina del paginado"
        assert "_prev" in paginado, "Error en '_prev' pagina del paginado"
        assert "_next" in paginado, "Error en  '_next' pagina del paginado"
        assert "_last" in paginado, "Error en '_last' pagina del paginado"

def test_listar_usuarios_404():
    url = "http://localhost:5001/account/999"

    result = requests.get(url)
    response = result.json()
    status = result.status_code

    assert status == 404, "Error al devolver un estado 404"
    assert "errors" in response , "Error se debe devolver un litado de 'errors'" 

    if response["errors"][0]:
        errors = response["errors"][0]
        assert "code" in errors, "Error no existe el elemento 'code' en errors"
        assert errors["code"] != [], "Error no 'code' no debe estar vacio"

        assert "message" in errors, "Error no existe el elemento 'message' en errors"
        assert errors["message"] != [], "Error no 'message' no debe estar vacio"

        assert "level" in errors, "Error no existe el elemento 'level' en errors"
        assert errors["level"] != [], "Error no 'level' no debe estar vacio"

        assert "description" in errors, "Error no existe el elemento 'description' en errors"
        assert errors["description"] != [], "Error no 'description' no debe estar vacio"


def test_listar_usuarios_400():
    _limit = -1
    _offset = -1
    url = f"http://localhost:5001/account?_limit='{_limit}'&'{_offset}'=2"

    result = requests.get(url)
    response = result.json()
    status = result.status_code

    assert status == 400, "Error al devolver un estado 400 con limit -1, off_set -1"
    #respuesta igual al 404



if __name__ == '__main__':
    # test_listar_usuarios_200()
    # print("ok")

    # test_listar_usuarios_404()
    # print("ok")
    
    test_listar_usuarios_400()
    print("ok")
