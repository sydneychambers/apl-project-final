import React from 'react';
import {Box, Flex} from '@chakra-ui/react';
import CodeEditor from './CodeEditor'; // Update the import statement
import ChatInterface from './ChatInterface';
import Header from './Header';
import Output from './Output';

function App() {
    return (
        <Box minH="100vh" bg="#21252B" color="gray.500" px={6} py={8}>
            <Box mb={0}>
                <Header/>
            </Box>
            <Flex justifyContent="center" width="100%" maxHeight="800px">
                <Box width="35%" height="100%">
                    <ChatInterface/>
                </Box>
                <Box width="65%" ml={4} height="100%">
                    <Box direction="column">
                        <CodeEditor/>
                    </Box>
                </Box>
            </Flex>


        </Box>
    );
}

export default App;
