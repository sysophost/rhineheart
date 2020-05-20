# Rhineheart
A modular rewrite of [neo-scripts](https://github.com/sysophost/neo-scripts)

At some point I'll add some more functionality to this.

---

## Usage
Print the help with `python rhineheart.py -h`

`--markobjects / -mo`

Mark the objects suppled with `--inputfile` as Owned, High Value, or both

*The input file can contain any objects, though only those that are matched in the database will be updated*

Valid options: 
* owned - mark supplied objects as Owned
* highvalue - mark supplied objects as High Value
* both - mark supplied objects as both Owned and High Value

**Requires `--inputfile`**

`--epochconvert / -ec`

Convert timestamps at the specified column index (set with `--col`) in the file supplied with `--inputfile` to a human readable format

*Date format can be optionally set with `--dateformat`*

**Requires `--inputfile` and `--col`**

`--col / -c`

Specify the column index to be used by `--epochconvert` 

*Can be specified multiple times using `-col 1 -col 2 -col n`*

`--findold / -fo`

Search for objects with either last logon or password last set older than a certain number of days (defined with `--days`)

Valid options: 
* logon - last logon
* password - password last changed

**Requires `--days`**

`--days / -d`

Number of days since the current date (**Required by `--findold`**)

`--inputfile`

Path to the input file (**Required by `--markobjects` and `--epochconvert`**)

*Objects must be formatted using the syntax `NAME@DOMAIN`*

### Optional Args
`--outputfile / -of`

Path to output file

`--dateformat / -df`

Specify the output date format to use (defaults to `%H:%M:%S %d/%m/%Y`)

Valid options: 
* short - `%d/%m/%Y`
* us - `H:%M:%S %m/%d/%Y`
* usshort - `%m/%d/%Y`

`--indelim / -id`

Use in conjunction with `--inputfile` to specify the file delimiter to use (defaults to `,`)

*if you want to use tab as a delimiter you have to specify it as `--indelim $'\t'`*

`--outdelim / -od`

Use in conjunction with `--outputfile` to specify the file delimiter to use (defaults to `,`)

*if you want to use tab as a delimiter you have to specify it as `-outdelim $'\t'`*

`--noheaders / -nh`

Prevent header row from being written to screen when using `--verbose`


`--timeout / -t`

Timeout for HTTP requests to Neo4j (defaults to 30 seconds)

`--verbose / -v`

Displays verbose output messages. 

At the moment this is the same output that would be written to file with `--outputfile`

This is really only useful if you want to redirect tool output to the clipboard or another tool

### DB Args
`--dbhost / -dh`

IP address or hostname where Neo4j is currently listening (defaults to `127.0.0.1`)

`--dbport / -dp`

Neo4j HTTP API listening port (defaults to `7474`)

`--username / -u`

Username to authenticate to Neo4j (defaults to `neo4j`)

`--password / -p`

Password to authenticate to Neo4j (defaults to `Pa55w0rd`)