from django.core.paginator  import Paginator


post=["1","2","3","4"]
p= Paginator(post,3)
# print(p.num_pages)

# for i in p.page_range:
#     print(i)


p1= p.page(1)
# print(p1)
# print(p1.number)
print(p1.object_list)
print(p1.has_next())
print(p1.next_page_number())
