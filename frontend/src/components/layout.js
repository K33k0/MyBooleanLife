import * as React from 'react'
import pageStyles from '../styles/pageStyle'
import CssBaseline from '@mui/material/CssBaseline';

import Grid from '@mui/material/Unstable_Grid2'
import MyBottomNavigation from './myBottomNav'
import { Paper } from '@mui/material'
import DrawerAppBar from './myAppBar';

const Layout = ({pageTitle, children}) => {
    return (
        <div>
            <CssBaseline />
            <DrawerAppBar/>
            <Grid container style={pageStyles}>
                <Grid xs={12}>
                    <header>
                        <h1>{pageTitle}</h1>
                    </header>
                </Grid>
                <Grid xs={12}>
                    <main container spacing={2}>{children}</main>
                </Grid>

            </Grid>
                {/* <Paper elevation={3} sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }}>
                    <footer>
                        <MyBottomNavigation/>
                    </footer>
                </Paper> */}
        </div>
    )
}
export const Head = () => <><meta name="viewport" content="initial-scale=1, width=device-width" /></>
export default Layout