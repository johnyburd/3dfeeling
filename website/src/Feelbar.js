import React from 'react'
import { withRouter } from 'react-router-dom'

import { Navbar, Nav } from 'react-bootstrap';
import logo from './logo.svg'

import DarkModeToggle from './Dark';

class Feelbar extends React.Component {

  render () {
      return (
        <div>
          <Navbar>
            <Navbar.Brand href="/">
              <img alt="" src={logo} width="32" height="32" className="d-inline-block align-top" />{' '}
              3D Feeling
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                <Nav.Link href="/">Home</Nav.Link>
                <Nav.Link href="/details">Details</Nav.Link>
                <DarkModeToggle/>
              </Nav>
            </Navbar.Collapse> 
          </Navbar>
        </div>
      )
    }
}

export default withRouter(Feelbar);