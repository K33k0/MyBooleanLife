import * as React from "react"
import AppBar from '@mui/material/AppBar';
import { Box, Divider, ListItem, ListItemButton,
     ListItemText, Typography, Toolbar, IconButton,
      Button, List, Drawer } from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import Link from "gatsby-plugin-material-ui";


const drawerWidth = 240;
const navItems = [
    <Link to="/" color="inherit">Home</Link>,
    <Link to="/about" color="inherit">About</Link>,
    <Link to="/tasks" color="inherit">Tasks</Link>
];

function DrawerAppBar(props) {
    const { window } = props
    const [mobileOpen, setMobileOpen] = React.useState(false);

    const handleDrawerToggle = () => {
        // Toggles the drawer state. 
        setMobileOpen((prevState) => !prevState);
    };

    const drawer = (
        <Box onClick={handleDrawerToggle} sx={{ textAlign: 'centre' }}>
            <Typography variant="h6" ssx={{ my: 2 }}>
                My Boolean Life
            </Typography>
            <Divider />
            <List>
                {navItems.map((item) => (
                    <ListItem key={item} disablePadding>
                        <ListItemButton sx={{ textAlign: 'centre' }}>
                            <ListItemText primary={item} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </Box>
    )

    const container = window !== undefined ? () => window().document.body : undefined;

    return (
        <Box sx={{ display: 'flex' }}>
            <AppBar component="nav">
                <Toolbar>
                    <IconButton 
                    color="inherit" 
                    aria-label="open drawer" 
                    edge="start" 
                    onClick={handleDrawerToggle} 
                    sx={{ mr: 2, display: { sm: 'none' } }}>
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}>
                        My Boolean Life
                    </Typography>
                    <Box sx={{ display: {xs: 'none', sm:'block'}}}>
                        {navItems.map((item) => (
                            <Button key={item} sx={{color: '#fff'}}>
                                {item}
                            </Button>
                        ))}
                    </Box>
                </Toolbar>
            </AppBar>
            <Box component="nav">
                <Drawer container={container} variant="temporary" open={mobileOpen} onClose={handleDrawerToggle} modalProps={{keepMounted:true}} sx={{display: {xs:'block', sm:'none'}, '& .MuiDrawer-paper': {boxSizing: 'border-box', width:drawerWidth},}}>
                    {drawer}
                </Drawer>
            </Box>
        </Box>
    )
}
export default DrawerAppBar;