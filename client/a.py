import client 
import time

c = client.Client(
    server_addr='127.0.0.1',
    server_port=1337,
    user_name='test1', 
    passwd = 'test1',
    email='test1',
    port=4000
)

c.sign_in()
c.log_in()
print(c.add_contact("kwitnoncy"))
print(c.add_contact("rojber"))
print(c.add_contact("test_wrong"))

print(c.modify_contact("kwitnoncy", {"name": "Piotr Kwiatkowski", "note": "kolega"}))
print(c.modify_contact("rojber", {"name": "Robert Molenda", "note": "kolega"}))


print(c.get_contacts())

print('---------------------------------')

"""
call = c.make_call('client_b')
print(call)
time.sleep(1)
if call['status'] == 'OK':
    c.send_bye('client_b')

time.sleep(1)
print('---------------------------------')

call = c.make_call('client_b')
print(call)
time.sleep(1)
if call['status'] == 'OK':
    c.send_bye('client_b')
"""
print(c.change_passwd_email_on_server(passwd="test2"))

time.sleep(0.15)

print(c.log_out())

time.sleep(0.15)

print(c.update_user_data('test1', 'test2'))

time.sleep(0.15)

print(c.log_in())

time.sleep(0.15)

# print(c.close())
