Assumptions:
- I am having a txt file (calling it 'protocol_number_map.txt') of all the protocol_number mapping to the keyword (e.g. 6 -> TCP), if we have non-standard protocol_number, this can be updated in the txt file (Found a link to the 150 protocol numbers in the AWS link shared. http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)
- Flow data is version 2 only with fields seperated by <space> 


Input files path expected in the main section of the python code:
-  flow_log.txt -> containing the flow log 
- protocol_number_map.txt (as mentioned in the assumption)
- lookup.txt file -> containing the lookup table as given in the question


Output file:
- Is named as 'result.txt' and will be in the same directory as the python code file by default.


Test performed:
- Incorrect file paths -> code raises appropriate exception
- Random cases in both lookup.txt and flow_log.txt -> code performs normalization (convert to lower case)
- Since we assume flow data is of version 2 only, we expect exactly 14 fields seperated by <space>. If we encounter more anything other than 14 in a specific row of flow data, we discard the row assuming data is not correct

Instructions:
- If all the input files are in the same PWD as the python code, no modifications are needed to the path
- No non-default libraries are imported so should work with python 3.5+ (due to use of type hinting) my system is using python 3.11.4

Simply run: 'python3 assessment_code.py'  to get the result. In case system encounters any error, the code handles it using try exception statements.
