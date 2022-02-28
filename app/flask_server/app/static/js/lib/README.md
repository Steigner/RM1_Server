## Note

Javascript libraries are zipped in the archive. To unzip:

```console
user@user-pc:~$ unzip lib.zip
```

For use just change in html:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/roslibjs/1.1.0/roslib.min.js" integrity="sha512-x2Owc9WayRcRj80Znkau58shVfXN2OIX+gQAlrx6KPugZBKrIC6AwgEWQQCI06p2Q8RB4ilxD+y+1BdNd+1fQA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

```

To:

```html
<script src="{{ url_for('static', filename='js/lib/roslib.min.js') }}"></script>
```
