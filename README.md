# Accio
Quickly summon a new web server 

Accio can handle any request method type that you define as well as delays to simulate network latency. If you have wildcards in your url path for example `/myPath/has/ID/152/page/endpoint/111` where 152 and 111 are wildcard paths then you can replace them in the config with `{$}` for example `/myPath/has/ID/{$}/page/endpoint/{$}`


Accio</br>
Author: Athony Russell</br>
Twitter: @DotNetRussell</br>
Blog: https://DotNetRussell.com</br>
GitHub: https://github.com/DotNetRussell</br>
</br>
To Use:</br>
</br>
python accio.py [config file path] [target localhost port] [calling port (For CORS)]</br>
</br>
Example:</br>
</br>
python accio.py /home/user/Desktop/accioConfig.json 8080 4200</br>
</br>
Example Output:</br>
</br>
Accio --% ~~~~ @X@ Server Active @X@</br>
Server Listening On Port 8080</br>
Press CTRL+C to stop the server
<br/>
<br/>
Example Config:</br>
```
{
        "routes" : [
                {
                        "url" : "/endpoint1",
                        "definition" : {
                                "filePath" : "./examples/endpoint1.json",
                                "method" : "GET",
                                "delay" : 5
                        }
                },
                {
                        "url" : "/endpoint1",
                        "definition" : {
                                "filePath" : "./examples/endpoint1_post.json",
                                "method" : "POST",
                                "delay" : 2
                        }
                },
                {
                        "url" : "/endpoint2",
                        "definition" : {
                                "filePath" : "./examples/endpoint2.json"

                        }
                },
                {
                        "url" : "/endpointWithWildCard/{$}/somethingElse/{$}",
                        "definition" : {
                                "filePath" : "./examples/wildCard.json"

                        }
                }

        ]

}

```
