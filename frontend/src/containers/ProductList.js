import React from 'react'
import { Image, Item } from 'semantic-ui-react'

const paragraph = <Image src='/images/wireframe/short-paragraph.png' />

class ProductList extends React.Component{
    render() {
        return(
            <Item.Group>
                <Item>
                <Item.Image size='tiny' src='/images/wireframe/image.png' />

                <Item.Content>
                    <Item.Header>Arrowhead Valley Camp</Item.Header>
                    <Item.Meta>
                    <span className='price'>$1200</span>
                    <span className='stay'>1 Month</span>
                    </Item.Meta>
                    <Item.Description>{paragraph}</Item.Description>
                </Item.Content>
                </Item>
            </Item.Group>
        );
    }
}

export default ProductList;