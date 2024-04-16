import React, {useState, useRef} from 'react';
import {VscCode} from "react-icons/vsc";
import {Box, Button, Flex, Tooltip} from "@chakra-ui/react";
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-chaos'; // Changed theme to 'chaos'
import {VscAdd} from "react-icons/vsc";
import {LuPlay} from "react-icons/lu";
import {FaRegSave} from "react-icons/fa";
import {RiDeleteBin6Line} from "react-icons/ri";
import Output from "./Output";

const CodeEditor = () => {
    const [code, setCode] = useState("");
    const [output, setOutput] = useState(null);
    const fileInputRef = useRef(null);
    const editorRef = useRef(null);


    const handleChange = (newValue) => {
        setCode(newValue);
    };

    const handleRun = async () => {
    try {
        // Get the current value of the AceEditor
        let code = getCodeFromEditor();

        // Sanitize the code to remove any unwanted characters
        code = code.replace(/\r/g, ''); // Remove carriage return characters


        // Send a POST request to the Flask backend
        const response = await fetch('/arya_compiler_endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Convert the response to text
        const data = await response.text();

        // Display the result
        console.log(data);
        setOutput(data);
    } catch (error) {
        console.error('Error:', error);
        setOutput("Error occurred: " + error.message);
    }
};


const getCodeFromEditor = () => {
    const editor = editorRef.current.editor;
    const code = editor.getValue();
    return code;
};

const handleSave = () => {
    const blob = new Blob([code], {type: 'text/plain'});
    const a = document.createElement('a');
    const url = URL.createObjectURL(blob);
    a.href = url;
    a.download = 'console_text.arya'; // Change the file extension to .arya
    a.click();
    URL.revokeObjectURL(url);
};

const handleClear = () => {
    setCode(""); // Clear the console by setting the code state to an empty string
};

const handleImport = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.arya')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            setCode(e.target.result);
        };
        reader.readAsText(file);
    } else {
        // Handle error: invalid file format
        console.error('Invalid file format. Please select a .arya file.');
    }
};

return (
    <div>
        <Box border="2px solid" borderRadius="md" p={3} mb={0} borderColor="gray.500">
            <Flex justifyContent="space-between" alignItems="center" mb={0}>
                <Box borderColor="gray.500" pb={0} mb={4} display="flex" alignItems="center">
                    <VscCode className="icon" color="#03aeed" size={30}/>
                    <div className="editor-text" style={{fontSize: '22px', marginLeft: '5px', color: 'white'}}>Console
                    </div>
                </Box>
                <Flex>
                    <Tooltip label="Import Files">
                        <Button
                            color="#03aeed"
                            isLoading={false}
                            variant="outline"
                            border="0px solid"
                            mb={4}
                            onClick={() => fileInputRef.current.click()}
                        >
                            <VscAdd size={20} style={{marginRight: '2px'}}/>
                        </Button>
                    </Tooltip>
                    <Tooltip label="Run Code">
                        <Button
                            color="green"
                            isLoading={false}
                            variant="outline"
                            border="0px solid"
                            mb={4}
                            onClick={handleRun}
                        >
                            <LuPlay size={20} style={{marginRight: '2px'}}/>
                        </Button>
                    </Tooltip>
                    <Tooltip label="Save Code">
                        <Button
                            color="orange"
                            isLoading={false}
                            variant="outline"
                            border="0px solid"
                            mb={4}
                            ml={2}
                            onClick={handleSave}
                        >
                            <FaRegSave size={20} style={{marginRight: '2px'}}/>
                        </Button>
                    </Tooltip>
                    <Tooltip label="Clear Console">
                        <Button
                            color="red"
                            isLoading={false}
                            variant="outline"
                            border="0px solid"
                            mb={4}
                            ml={2}
                            onClick={handleClear}
                        >
                            <RiDeleteBin6Line size={20} style={{marginRight: '2px'}}/>
                        </Button>
                    </Tooltip>
                </Flex>
            </Flex>
            <Box mb={4}>
                <AceEditor
                    ref={editorRef}
                    mode="python"
                    theme="chaos" // Changed theme to 'chaos'
                    value={code}
                    onChange={handleChange}
                    width="100%"
                    height="45vh"
                    fontSize={16}
                    showPrintMargin={true}
                    showGutter={true}
                    highlightActiveLine={true}
                    setOptions={{
                        enableBasicAutocompletion: true,
                        enableLiveAutocompletion: true,
                        enableSnippets: true,
                        showLineNumbers: true,
                        tabSize: 4,
                    }}
                />
            </Box>
        </Box>
        <Box mt={2}>
            <Output output={output}/>
        </Box>
    </div>
);
}
;

export default CodeEditor;
