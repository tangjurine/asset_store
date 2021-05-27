import json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}
dataset_1 = [
    {
        'name': 'TEST_' + str(i),
        'type': 'satellite',
        'class': 'dove'
    } for i in range(1, 7)
]

dataset_2 = [
    {
        'name': '_TEST__',
        'type': 'satellite',
        'class': 'dove'
    },
    {
        'name': '-TEST__',
        'type': 'satellite',
        'class': 'dove'
    },
    {
        'name': 'TEST-_',
        'type': 'satellite',
        'class': 'yagi'
    },
    {
        'name': 'TEST-_',
        'type': 'antenna',
        'class': 'rapideye'
    },
    {
        'name': 'TEST-_',
        'type': 'satellite',
        'class': 'skysat'
    },
    {
        'name': 'TEST-_test123123',
        'type': 'antenna',
        'class': 'dish'
    }
]

def test_get_all(app, client):
    response = client.get('/')
    assert response.status_code == 200
    assert [] == json.loads(response.get_data(as_text=True))

    client.post('/add', data=json.dumps(dataset_1[0]), headers=headers)

    response = client.get('/')
    assert response.status_code == 200
    assert [dataset_1[0]] == json.loads(response.get_data(as_text=True))

def test_add(app, client):
    response = client.post('/add', data=json.dumps(dataset_1[0]), headers=headers)
    assert '' == response.get_data(as_text=True)
    assert response.status_code == 201

def test_add_duplicate(app, client):
    response = client.post('/add', data=json.dumps(dataset_1[0]), headers=headers)
    assert '' == response.get_data(as_text=True)
    assert response.status_code == 201

    response = client.post('/add', data=json.dumps(dataset_1[0]), headers=headers)
    assert 'name of asset already exists' == response.get_data(as_text=True)
    assert response.status_code == 400

def test_page(app, client):
    for d in dataset_1:
        response = client.post('/add', data=json.dumps(d), headers=headers)
        assert '' == response.get_data(as_text=True)
        assert response.status_code == 201
    response = client.get('/')
    assert response.status_code == 413

    response = client.get('/page/50')
    assert response.status_code == 400
    assert 'invalid query parameter: page' == response.get_data(as_text=True)

    response = client.get('/page/0')
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        'current_page': 0,
        'total_pages': 2,
        'assets': dataset_1[0:5]
    }

def test_get(app, client):
    for d in dataset_1:
        response = client.post('/add', data=json.dumps(d), headers=headers)
        assert '' == response.get_data(as_text=True)
        assert response.status_code == 201
    response = client.get('/name/TEST_1')
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == dataset_1[0]

    response = client.get('/name/foobar')
    assert response.status_code == 404
    assert 'name not found' == response.get_data(as_text=True)

def test_invalid_data(app, client):
    for idx, d in enumerate(dataset_2):
        response = client.post('/add', data=json.dumps(d), headers=headers)
        if idx < 4:
            assert response.status_code == 400
            assert 'invalid asset' == response.get_data(as_text=True)
        else:
            assert response.status_code == 201
            assert '' == response.get_data(as_text=True)
    response = client.get('/')
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == dataset_2[4:]
        
