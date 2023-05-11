import * as React from 'react'
import Block from '../components/block'
import Layout from '../components/layout'

const aboutPage = () => {
    return (
        <Layout pageTitle="About">
        <div>
            <Block name="09/05/2023"/>
            <Block name="10/05/2023"/>
            <Block name="11/05/2023"/>
        </div>
        </Layout>
    )
}

export const Head = () => <title>about My Boolean Life</title>
export default aboutPage