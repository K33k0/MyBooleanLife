import React from 'react';
import { Link } from 'gatsby';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';


const MyBottomNavigation = () => {
    const [value, setValue] = React.useState(0);
    return (
        <BottomNavigation showLabels value={value} onChange={(event, newValue) => {setValue(newValue);}}>
            <BottomNavigationAction label="Home" component={Link} to="/"/>
            <BottomNavigationAction label="About"component={Link} to="/about"/>
        </BottomNavigation>
    )
}

export default MyBottomNavigation