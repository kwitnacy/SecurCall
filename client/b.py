import client


c = client.Client(
    server_addr='127.0.0.1',
    server_port=1337,
    user_name='client_b', 
    passwd = 'test_pass_client_b',
    email='test_email_b',
    port=4200
)

c.sign_in()
c.log_in()

print(c.get_history())

time.sleep(6)
print(c.send_bye('test1'))

