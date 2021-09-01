import { Navbar, Container } from "react-bootstrap";

const Header = () => {
  return (
    <Navbar bg="primary" variant="dark">
      <Container>
        <Navbar.Brand href="/">
          デジコア2.0
        </Navbar.Brand>
      </Container>
    </Navbar>
  )
}

export default Header;