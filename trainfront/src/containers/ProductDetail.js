import React from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import axios from "axios";
import {
  Button,
  Card,
  Container,
  Dimmer,
  Form,
  Grid,
  Header,
  Icon,
  Image,
  Item,
  Label,
  Loader,
  Message,
  Segment,
  Select,
  Divider
} from "semantic-ui-react";
import { productDetailURL, addToCartURL } from "../constants";
import { fetchCart } from "../store/actions/cart";
import { authAxios } from "../utils";

class ProductDetail extends React.Component {
  state = {
    loading: false,
    error: null,
    formVisible: false,
    data: [],
    formData: {}
  };

  componentDidMount() {
    this.handleFetchItem();
  }

  handleToggleForm = () => {
    const { formVisible } = this.state;
    this.setState({
      formVisible: !formVisible
    });
  };

  handleFetchItem = () => {
    const {
      match: { params }
    } = this.props;
    this.setState({ loading: true });
    axios
      .get(productDetailURL(params.productID))
      .then(res => {
        this.setState({ data: res.data[0], loading: false });
      })
      .catch(err => {
        this.setState({ error: err, loading: false });
      });
  };

  handleFormatData = formData => {
    // convert {colour: 1, size: 2} to [1,2] - they're all variations
    return Object.keys(formData).map(key => {
      return formData[key];
    });
  };

  handleAddToCart = () => {
    this.setState({ loading: true });
    const { formData } = this.state.data;
    const variations = this.handleFormatData(formData);
    authAxios
      .post(addToCartURL, { variations })
      .then(res => {
        this.props.refreshCart();
        this.setState({ loading: false });
      })
      .catch(err => {
        this.setState({ error: err, loading: false });
      });
  };

  handleChange = (e, { name, value }) => {
    const { formData } = this.state;
    const updatedFormData = {
      ...formData,
      [name]: value
    };
    this.setState({ formData: updatedFormData });
  };

  render() {
    const { data, error, formData, formVisible, loading } = this.state;
    const item = data;
    return (
   
      <Container>
        {error && (
          <Message
            error
            header="There was some errors with your submission"
            content={JSON.stringify(error)}
          />
        )}
        {loading && (
          <Segment>
            <Dimmer active inverted>
              <Loader inverted>Loading</Loader>
            </Dimmer>
            <Image src="/images/wireframe/short-paragraph.png" />
          </Segment>
        )}
        <Grid columns={2} divided>
          <Grid.Row>
            <Grid.Column>
              <Card
                fluid
                image={item.thumbnail}
                header={item.name}
                meta={
                  <React.Fragment>
                    {item.category}
                      <Label color="green">
                        {}
                      </Label>
                  </React.Fragment>
                }
                description={item.description}
                extra={
                  <React.Fragment>
                    <Button
                      fluid
                      color="yellow"
                      floated="right"
                      icon
                      labelPosition="right"
                      onClick={this.handleToggleForm}
                    >
                      Add to cart
                      <Icon name="cart plus" />
                    </Button>
                  </React.Fragment>
                }
              />
              {formVisible && (
                <React.Fragment>
                  <Divider />
                  <Form onSubmit={() => this.handleAddToCart}>
                        <Form.Field>
                          <Select
                            onChange={this.handleChange}
                            placeholder={`Select a variant`}
                            fluid
                            selection
                            options={data.variants.map(item => {
                              return {
                                key: item.id,
                                text: item.__str__,
                                value: item.id
                              };
                            })}
                            value={formData["0"]}
                          />
                        </Form.Field>
                    <Form.Button primary>Add</Form.Button>
                  </Form>
                </React.Fragment>
              )}
            </Grid.Column>
            {/* <Grid.Column>
              <Header as="h2">Try different variations</Header>
              {data.variants.map(v => {
                  return (
                    <React.Fragment key={v.id}>
                      <Header as="h3">{v.__str__}</Header>
                      <Item.Group divided>
                        {data.variants.map(iv => {
                          return (
                            <Item key={iv.id}>
                              {iv.thumbnail && (
                                <Item.Image
                                  size="tiny"
                                  src={iv.thumbnail}
                                />
                              )}
                              <Item.Content verticalAlign="middle">
                                {iv.price}
                              </Item.Content>
                            </Item>
                          );
                        })}
                      </Item.Group>
                    </React.Fragment>
                  );
                })}
            </Grid.Column> */}
          </Grid.Row>
        </Grid>
      </Container>
    );
  }
}

const mapDispatchToProps = dispatch => {
  return {
    refreshCart: () => dispatch(fetchCart())
  };
};

export default withRouter(
  connect(
    null,
    mapDispatchToProps
  )(ProductDetail)
);
