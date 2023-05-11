import * as React from 'react'
import { Link } from 'gatsby'
import pageStyles from '../styles/pageStyle'

const Layout = ({pageTitle, children}) => {
    return (
        <div style={pageStyles}>
            <header>
                <h1>{pageTitle}</h1>
                <nav>
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/about">About</Link></li>
                </ul>
            </nav>
                {children}
            </header>
            <main></main>
            <footer>My Boolean Life, by Kieran Wynne</footer>
        </div>
    )
}
export default Layout