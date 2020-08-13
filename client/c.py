import client


c = client.Client(
    server_addr='127.0.0.1',
    server_port=1337,
    user_name='client_b', 
    passwd = 'test_pass_client_b',
    email='test_email_b',
    port=4400
)

c.sign_in()
c.log_in()
# c.make_call('client_b')


