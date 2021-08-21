//記事表示ﾍﾟｰｼﾞ
import { GetStaticProps, GetStaticPaths, GetServerSideProps, } from 'next'
import { axios } from '../../utils/axios';
import { Markdown } from '../../components/Markdown';
import PageHead from '../../components/PageHead';
import { Container, Row } from 'react-bootstrap';
import { Article, ArticleTag } from '../../interfaces/index'

const baseURL = process.env.NODE_ENV === 'production' ? 'https://core.digicre.net' : 'http://localhost:8000'

const ArticlePage = (props: ArticlePageProps) => (
  <Container>
    <PageHead title={props.data.title} description={props.data.content} img={`${baseURL}/blog/article/${props.data.id}/ogp_image`} />
    <Row>
    <h1 style={{borderBottom: 'solid 2px #87CEFA'}}>{props.data.title}</h1>
    </Row>
    <Row style={{display:'inline-block', marginLeft:'10px'}}>
      {props.tags.map(tag=>(
        <span className='badge rounded-pill bg-primary'>{tag.name}</span>
      ))}
    </Row>
    <Markdown md={props.data.content}></Markdown>
  </Container>
)

export default ArticlePage

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const id = params?.id;
    const resData = axios.get('/blog/articles/' + String(id))
    const data: Article = (await resData).data;
    const tags: ArticleTag[] = await Promise.all(data.article_tags.map(async tagId=>
      (await axios.get('/blog/article_tag/' + String(tagId))).data
    ))
    return { props: { data, tags } }
  } catch (error) {
    return { props: { errors: error.message } };
  }
};

type ArticlePageProps = {
  data?: Article
  tags?: ArticleTag[]
  errors?: any
}
