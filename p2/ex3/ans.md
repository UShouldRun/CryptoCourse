**Q3.1**: Explain what the following command is doing, and how the different flags influence its behavior.

```
$ hexdump -n 32 -e '1/4 "%0X" 1 "\n"' /dev/urandom
```

This command is reading from the Linux **/dev/urandom** file, which is a special file that provides random numbers. **hexdump** will output the hexadecimal string representing those numbers, since most of them are not ASCII characters. 

These flags are used to only read 32 bytes from the file and to format the output as follows: consume the input in 4 bytes chunks and make the characters uppercase. For example:   

```
872ED08B
48CD3C2C
9F665E38
D93669B7
F075A13E
7929577D
5D60857E
43A4FBA5
```

**Q3.2**: Use OpenSSL's rand operation as an alternative. Describe the command that must be executed.

The command can be:

```openssl rand -hex 32 | fold -w 8```

It will output 32 bytes as hex and output that into the **fold** command, wich will break the output in lines of 8 characters (representing 4 bytes). For example:


```
0f2b8322
5af6aee5
e46f7320
f7120eb6
f409dabe
763bbc7b
dca06eae
93c4c907
```

To get uppercase character we could add the **tr** command, swapping lowercase by uppercase.

```
openssl rand -hex 32 | tr [:lower:] [:upper:]| fold -w 8
```
