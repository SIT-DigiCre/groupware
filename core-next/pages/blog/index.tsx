import { ReactEventHandler, useState, useEffect } from "react";
import { Button, Fab, TextField, Grid, TableCell, TableHead, Table, TableRow, TableContainer, Paper, TableBody, IconButton } from "@mui/material";
import { axios } from "../../utils/axios";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import useSWR from "swr";
import { Article, ArticleTag, ArticleList } from "../../interfaces/blog";
import Breadcrumbs from "../../components/Common/Breadcrumbs";
import EditIcon from '@mui/icons-material/Edit';
import InfiniteScroll from "react-infinite-scroller";

const BlogIndexPage = () => {
  const token = useSelector((state: RootState) => state.token.token);
  const [articles, setArticles] = useState<Article[]>([]);
  const [articleNextUrl, setArticleNextUrl] = useState("");
  const [newMode, setNewMode] = useState(false);
  const loader = (
    <div className="loader" key={0}>
      Loading ...
    </div>
  );
  const loadNext = async () => {
    if (articleNextUrl === "") return;
    const resData = axios.get(articleNextUrl);
    const data: ArticleList = (await resData).data;
    setArticleNextUrl(data.next);
    setArticles(articles.concat(data.results));
  };
  const fetcher = (url: string, token: string | null) => {
    if (token) {
      axios
        .get(url, { headers: { Authorization: "JWT " + token } })
        .then((res) => {
          setArticles(res.data.results);
          setArticleNextUrl(res.data.next);
          return res.data;
        });
    } else {
      return null;
    }
  };
  const { data } = useSWR(["/v1/blog/my_article/", token.jwt], fetcher);
  useEffect(() => {
    if (data) {
      setArticles(data.result);
      setArticleNextUrl(data.next);
    }
  }, [data]);
  console.log(data)
  return (
    <Grid container alignItems="center" justifyContent="center">
      <Grid item xs={11}>
        <Breadcrumbs links={[{ name: "Blog" }]} />
        <Paper>
          <Button
            variant="contained"
            href="/blog/new"
            style={{ margin: "5px" }}>
            New Article
          </Button>
        </Paper>
        <h1>My Articles</h1>
        <InfiniteScroll
          loadMore={loadNext}
          hasMore={articleNextUrl !== null}
          loading={loader}
        >
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 450 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>ファイル名</TableCell>
                  <TableCell align="right">作成日</TableCell>
                  <TableCell align="right">編集</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>

                {articles.map((article) => (
                  <TableRow
                    key={article.id}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      <a href={"https://blog.digicre.net/article/" + String(article.id)}>{article.title}</a>
                    </TableCell>
                    <TableCell align="right">{article.pub_date}</TableCell>
                    <TableCell align="right">
                      <IconButton
                        aria-label="edit"
                        href={"/blog/edit?articleId=" + String(article.id)}
                      >
                        <EditIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}

              </TableBody>
            </Table>
          </TableContainer>
        </InfiniteScroll>
      </Grid>
    </Grid>
  );
};

export default BlogIndexPage;
