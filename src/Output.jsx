import React, {useRef, useState} from 'react';
import {Box, Button, Text, useToast} from "@chakra-ui/react";
import {VscTerminal} from "react-icons/vsc";

const Output = ({output}) => {
    const outputRef = useRef(null);

    return (
        <Box border="2px solid" borderRadius="md" p={4} mb={4} borderColor="gray.500">
            <Box borderColor="gray.500" pb={0} mb={4} display="flex" alignItems="center">
                <VscTerminal className="icon" color="#03aeed" size={30}/>
                <div className="terminal-text" style={{fontSize: '22px', marginLeft: '5px', color: 'white'}}>Terminal
                </div>
            </Box>
            <Box
                ref={outputRef}
                height="39vh"
                p={2}
                border="2px solid"
                borderRadius={4}
                borderColor="gray.500"
                style={{overflowY: 'auto'}}
            >
                <Text style={{color: 'white'}}>{output}</Text>
            </Box>
        </Box>
    );
};

export default Output;

