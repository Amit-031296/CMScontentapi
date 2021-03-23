<h1>Build a REST API for Cms system</h1>

<p>This is the REST API for a cms system by using django rest framework.</p>

<p><strong>In this CMS Rest API I have Implemented Following Things: </strong></p>
<ul>
<li>User authentication via Django "TokenAuthentication"</li>
<li>Generating Auth Tokens</li>
<li>Create Admin Using Seeding</li>
<li>Apply Field Level Validation</li>
<li>
CRUD functionality on a Content:<br>
<ol>
<li>Create Contents</li>
<li>Retrieve Contents</li>
<li>Update Contents</li>
<li>Delete Contents</li>
</ol>
</li>
<li>Serialization of data</li>
<li>JSON</li>
</ul>
<li>
Steps for setup the Project and Run it <br>
<ol>
<li>Activate the Virtual Env (in directory src/env): cd env/Scripts and [activate]<li>

<li>For Creating Admin using Seeding:</li>
<li>run the Command "python manage.py loaddata seed_data/seed.json"[Change the Json File Fields,pk Value and all the Fields in Json] one of the superuser is username="admin@gmail.com" and Password="admin" </li>

<li>For Registering New Author:</li>
<li>Url = "http://127.0.0.1:8000/api/account/register"</li>
<li>Field to be Passed [email,username,user_firstname,user_lastname,user_phone_number,user_address,user_city,user_state,user_country,user_pincode,password,password2]</li>
<li>Field Level Validation Used:</li>
<p>Email std validation</p>
<p>password min 8 length 1uppercase 1 lowercase</p>
<p>phone number</p>
<p>user pincode</p>

<li>Create New Content</li>
<li>Url = "http://127.0.0.1:8000/api/content/create"</li>
<li>Headers: Authorization: Token "Token_value"</li>
<li>Field to be Passed [content_title,content_body,content_summary,content_file_pdf,content_category</li>
<li>Field Level Validation Used:</li>
<p>content_title has max length of 30</p>
<p>content_body has max length of 300</p>
<p>content_summary has max length of 60</p>
<p>content_file_pdf has to be pdf file</p>


<li>Retrieve Contents</li>
<li>Url = "http://127.0.0.1:8000/api/content/list"[GET]</li>
<li><strong>If You Are Logged in as Admin(superuser)</strong></li>
<li>Headers: Authorization: Token "Token_value"</li>
<li>1) list: http://127.0.0.1:8000/api/content/list
2) pagination: http://127.0.0.1:8000/api/content/list?3) search: http://127.0.0.1:8000/api/content/list?search=admin
4) ordering: http://127.0.0.1:8000/api/content/list?ordering=-date_updated
4) search + pagination + ordering: http://127.0.0.1:8000/api/content/list?search=admin&page=2&ordering=-date_updated</li>
<li>Url = "http://127.0.0.1:8000/api/content/list_content_of_user"[GET]</li>

<li>Url = "http://127.0.0.1:8000/api/content/list_content_of_user"[GET]</li>
<li><b>If You Are Logged in as Author</b></li>
<li>Headers: Authorization: Token "Token_value"</li>



<li>Delete Contents</li>
<li>Url = "http://127.0.0.1:8000//api/content/slug/delete"[DELETE]</li>
<li>Headers: Authorization: Token "Token_value"</li>

<li>Check Is Author of that Content</li>
<li>Url = "http://127.0.0.1:8000//api/content/slug/is_author"[GET]</li>
<li>Headers: Authorization: Token "Token_value"</li>


</ol>
</li>

