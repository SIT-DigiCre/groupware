import { axios } from "../../utils/axios";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import useSWR from "swr";
import { useEffect } from "react";

const fetcher = async(url: string, token: string|null) => {
  if(token){
    const res = await axios.get(url, {
      headers: { Authorization: "JWT " + token },
    }).then(res => {
      return res.data;
    }).catch(error=>{
      return null;
    });
  }else{
    return null;
  }
}
const StorageIndexPage = () => {
  const user = useSelector((state: RootState) => state.user.user);
  const token = useSelector((state: RootState) => state.token.token);
  const { data } = useSWR(["/v1/work/item", token.jwt], fetcher);
  return (
    <>
      
    </>
  );
}
export default StorageIndexPage;