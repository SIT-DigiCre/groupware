import Link from 'next/link'
import { GetServerSideProps } from 'next'
import { axios } from '../utils/axios'
import { string } from 'prop-types'
import { Article, ArticleList } from '../interfaces/blog'
import { Container, Card, Col, Row } from 'react-bootstrap';
import { Markdown } from '../components/Markdown';
import PageHead from '../components/PageHead';
import { getPreviewText } from '../utils/markdown-util'
import { baseURL } from '../utils/common'
import { useState, useEffect } from 'react'

const IndexPage = (props: { data: ArticleList }) => {
  const [articles, setArticles] = useState<Article[]>(props.data.results)
  let articlePreviousUrl = props.data.previous
  // react-infinite-scrollerを使用する
  return (
    <div>
      <PageHead title='デジクリブログ' description='芝浦工業大学 デジクリのブログサイト' />
      <Container className='mt-2'>
        <Row>
          <h3>デジクリブログ最新記事</h3>
        </Row>
        <Row>
          {articles.map(article => (
            <Col md={4} sm={6} className='mt-2'>
              <Link href={'/article/' + String(article.id)}>
                  <Card>
                  <Card.Img src={article.article_image !== '' ? article.article_image : `${baseURL}/blog/article/${article.id}/ogp_image`} height={200} style={{objectFit:'cover'}}></Card.Img>
                    <Card.Body>
                      <Card.Title>{article.title}</Card.Title>
                      <Card.Text>{getPreviewText(article.content, 120)}</Card.Text>
                    </Card.Body>
                  </Card>
                </Link>
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  )
}

export default IndexPage

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const resData = axios.get('/v1/blog/article');
    const data: ArticleList = (await resData).data;
    console.log(data)
    return { props: { data } }
  } catch (error) {
    return { props: { errors: error.message } };
  }
};