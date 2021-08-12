//記事表示ﾍﾟｰｼﾞ
import { GetStaticProps, GetStaticPaths, GetServerSideProps, } from 'next'
import { axios } from '../../utils/axios';
import { Markdown } from '../../components/Markdown';
import PageHead from '../../components/PageHead';
import { Container } from 'react-bootstrap';

const ArticlePage = (props) => (
  <Container>
    <PageHead title={props.data.title} description={props.data.content} />
    <h1>{props.data.title}</h1>
    <Markdown md={props.data.content}></Markdown>
  </Container>
)

export default ArticlePage

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const id = params?.id;
    const resData = axios.get('/blog/articles/' + String(id));
    const data = (await resData).data;
    console.log(data)
    return { props: { data } }
  } catch (error) {
    return { props: { errors: error.message } };
  }
};