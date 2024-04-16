import './Header.css';
import React from 'react';

const Header = () => {
    const headerStyle = {
        display: 'flex',
        justifyContent: 'center', // Horizontally center the content
        alignItems: 'center', // Vertically center the content
        height: '100px', // Adjust the height as needed
        paddingBottom: '50px', // Add padding to the bottom
    };

    return (
        <header style={headerStyle}>
            <img src="./icon2.png" alt="Arya Logo" style={{width: '100px', height: 'auto'}}/>
        </header>
    );
};

export default Header;
