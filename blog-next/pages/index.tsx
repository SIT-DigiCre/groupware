import Link from 'next/link'
import { GetServerSideProps } from 'next'
import { axios } from '../utils/axios'
import { string } from 'prop-types'
import { Article } from '../interfaces'
import { Container, Card } from 'react-bootstrap';
import { Markdown } from '../components/Markdown';
import PageHead from '../components/PageHead';

const IndexPage = (props: { data: Article[] }) => (
  <div>
    <PageHead title='デジコアブログ' description='芝浦工業大学 デジクリのブログサイト' />
    <Container>
      {props.data.map(article => (
        <Link href={'/article/'+String(article.id)}>
          <Card>
            <Card.Title>{article.title}</Card.Title>
            <Card.Body>{article.content}</Card.Body>
          </Card>
        </Link>
      ))}
      
    </Container>
  </div>
)

export default IndexPage

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const resData = axios.get('/blog/articles');
    const data: Article[] = (await resData).data;
    console.log(data)
    return { props: { data } }
  } catch (error) {
    return { props: { errors: error.message } };
  }
};