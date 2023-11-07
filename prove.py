

import User 

u=User.User(50)
u1=User.User(500)
u2=User.User(40)
u3=User.User(30)

us=[u,u1,u2,u3]
for u in us:
    print(u.data_size)

us.sort(key=lambda x: x.data_size/0.006,reverse=True)
print("\n")

for u in us:
    print(u.data_size)
