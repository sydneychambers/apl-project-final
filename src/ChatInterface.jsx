import React, {useState, useRef, useEffect} from "react";
import {Box, Input, Button, Text, Tooltip} from "@chakra-ui/react"; // Import Tooltip component
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-chaos";
import {SiSendinblue} from "react-icons/si";
import {FaCopy} from "react-icons/fa";

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [aiCode, setAiCode] = useState("");
    const [showAiCode, setShowAiCode] = useState(false);
    const inputRef = useRef(null);
    const editorRef = useRef(null);

    useEffect(() => {
        const currentTime = new Date().getHours();
        let greeting;
        if (currentTime < 12) {
            greeting = "Good morning! I'm the Arya Code Assistant. How can I help you today?";
        } else if (currentTime < 18) {
            greeting = "Good afternoon! I'm the Arya Code Assistant. How can I assist you?";
        } else {
            greeting = "Good evening! I'm the Arya Code Assistant. How can I assist you tonight?";
        }
        setMessages([{sender: "Arya Assistant", text: greeting}]);
    }, []);

    const handleSubmit = async () => {
    // Get the current value of the user input field
    const input_data = inputRef.current.value;

    // Clear the input field
    inputRef.current.value = '';

    const response = await fetch('/gemini_endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({input_data}),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Add user input to chat history
    setMessages(prevMessages => [...prevMessages, {sender: "You", text: input_data}])

    // Do something with the result
    console.log(data);
    handleAiResponse(data.output);
};


    const handleAiResponse = (response) => {
    // Add the AI response to the messages array
    setMessages(prevMessages => [
        ...prevMessages,
        { sender: "Arya Assistant", text: response }
    ]);
  };

    const copyCodeToClipboard = () => {
        const code = editorRef.current.editor.getValue();
        navigator.clipboard.writeText(code);
    };

    useEffect(() => {
        inputRef.current.focus();
    }, []);

    return (
        <Box mb={4} border="2px solid" borderColor="gray.500" borderRadius="md" p={4} width="100%" maxHeight="980px"
             position="relative">
            <Box mb={2} maxHeight="650px" overflowY="auto" border="2px solid" borderColor="gray.500" borderRadius="md"
                 p={4} position="relative">
                {messages.map((message, index) => (
                    <Box key={index} mb={2}>
                        <Text className={message.sender === "You" ? "user-message" : "ai-message"}
                              color={message.sender === "You" ? "white" : "#03aeed"}
                              fontWeight="bold">{message.sender}:</Text>
                        <Text color="white">{message.text}</Text>
                    </Box>
                ))}
                {showAiCode && (
                    <Box mb={4} maxHeight="500px" display="flex" justifyContent="center" position="relative">
                        <AceEditor
                            ref={editorRef}
                            height="500px"
                            width="100%"
                            mode="python"
                            theme="chaos"
                            value={aiCode}
                            readOnly={true}
                        />
                        <Button
                            onClick={copyCodeToClipboard}
                            position="absolute"
                            bottom="10px"
                            right="10px"
                            colorScheme="blue"
                            size="sm"
                            leftIcon={<FaCopy/>}
                        >
                            Copy
                        </Button>
                    </Box>
                )}
            </Box>
            <Box position="relative" bottom="0" left="0" width="100%">
                <Box display="flex">
                    <Input
                        id="user-input"
                        ref={inputRef}
                        placeholder="Type your message..."
                        border="2px solid"
                        borderColor="gray.500"
                        borderRadius="md"
                        flex="1"
                        marginRight="2"
                        onKeyDown={(e) => {
                            if (e.key === "Enter") handleSubmit();
                        }}
                    />
                    {/* Add Tooltip to the send button */}
                    <Tooltip label="Send Response" fontSize="md">
                        <Button color="#03aeed" border="0px solid" isLoading={false} variant="outline"
                                onClick={handleSubmit}>
                            <SiSendinblue size={25} style={{marginRight: '2px'}}/>
                        </Button>
                    </Tooltip>
                </Box>
            </Box>
        </Box>
    );
};

export default ChatInterface;
