Title: Python C Interaction using JSON
Date: 2014-04-06 13:48
Tags: C, JSON, Python
Slug: python-c-interaction-using-json
Status: published

[JSON](http://www.json.org/ "JSON site") can be used for communication
between python programs and C programs.
Python dictionaries can be transported to a C program which can then parse the
JSON and extract the relevant information. In this post a python to C program
communication using JSON is discussed.
For the python the native JSON package can be used. For the C program
json-c library (version 0.9) is used. Details about the json-c library can be
found in this
[link](https://github.com/json-c/json-c "json-c link").

The python script generates two JSON objects that are transferred to a C
program which retrieves them by reading its stdin.

The python code is listed below:

```python
import json

transfer_dict = {}
transfer_dict['command'] = 'start'

s = json.dumps(transfer_dict)
print s

inn_dict={}
nest_dict={}

inn_dict['step']="1"
inn_dict['value']="2"//
nest_dict['increment']=inn_dict

s = json.dumps(nest_dict)
print s
```

The output from the script is:

    $ python py_json.py
    {"command": "start"}
    {"increment": {"step": "1", "value": "2"}}

The first JSON is a simple string JSON with a value of "start" for the key
"command". The second JSON is a nested JSON with integer values for "step" and
"value".

The C program to read from stdin and parse and extract json values is
shown below:

```c
#include <stdio.h>
#include "json/json.h"

int main()
{
    struct json_object *jobj, *val_jobj;
    char const *val;
    char buf[50];

    fgets(buf, sizeof(buf), stdin);
    printf("Input JSON : %s", buf);

    //Parse the received JSON.
    jobj = json_tokener_parse(buf);
    if (is_error(jobj))
        return (-1);

    printf("Received JSON in String format : %s\n",
           json_object_to_json_string(jobj));

    //Get the value for the key "command"
    val_jobj = json_object_object_get(jobj, "command");
    printf("Extracted value for command : %s\n",
           json_object_to_json_string(val_jobj));

    //Get the string from the value of the key "command"
    val = json_object_get_string(val_jobj);
    printf("String value returned : %s\n", val);

    //Destroy the object now.
    json_object_put(jobj);

    fgets(buf, sizeof(buf), stdin);
    printf("Input JSON : %s", buf);

    jobj = json_tokener_parse(buf);
    if (is_error(jobj))
        return (-1);

    printf("Received JSON in String format : %s\n",
           json_object_to_json_string(jobj));

    val_jobj = json_object_object_get(jobj, "increment");
    printf("Extracted value for nested increment : %s\n",
           json_object_to_json_string(val_jobj));

    json_object_put(jobj);

    return 0;
}
```

The nested JSON can be extracted with this additional code.

```c
struct json_object *njobj;
int jint;

njobj = json_object_object_get(val_jobj, "step");
printf("Extracted value for step : %s\n",
       json_object_to_json_string(njobj));

//Get the Integer from the value of key "step"
jint = json_object_get_int(njobj);
printf("value returned : %d\n", jint);

json_object_put(njobj);

njobj = json_object_object_get(val_jobj, "value");
printf("Extracted value for value : %s\n",
       json_object_to_json_string(njobj));

jint = json_object_get_int(njobj);
printf("value returned : %d\n", jint);

json_object_put(njobj);
```

The C program can be compiled using gcc and reference to the json-c
library.

    $ gcc -Wall -I/Work/Contents/json-c-0.9/inst/include/ c_json.c -L/Work/Contents/json-c-0.9/inst/lib/ -ljson -o c_json

The output of the program (along with the extended parsing of the nested JSON)
is shown below.

    $ python py_json.py | ./c_json
    Input JSON : {"command": "start"}
    Received JSON in String format : { "command": "start" }
    Extracted value for command : "start"
    String value returned : start
    Input JSON : {"increment": {"step": "1", "value": "2"}}
    Received JSON in String format : { "increment": { "step": "1", "value": "2" } }
    Extracted value for nested increment : { "step": "1", "value": "2" }
    Extracted value for step : "1"
    value returned : 1
    Extracted value for value : "2"
    value returned : 2

The above post use the PIPE mechanism to transport JSON from python script to
C program.
Any sort of IPC including sockets, message queue etc can be used instead.
