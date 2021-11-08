import { axios } from "../../utils/axios";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import { WorkTag } from "../../interfaces/work";
import useSWR from "swr";
import { Autocomplete, TextField } from "@mui/material";

type Props = {
  onChange?: (event: any, value: WorkTag[]) => void;
};

const TagSelectBox = (props: Props) => {
  const token = useSelector((state: RootState) => state.token.token);
  const fetcher = async (url: string, token: string | null) => {
    if (token) {
      const res = await axios.get(url, {
        headers: { Authorization: "JWT " + token },
      });
      return res.data;
    } else {
      return null;
    }
  };
  const { data: tags } = useSWR<WorkTag[]>(
    [`/v1/work/tag/`, token.jwt],
    fetcher
  );
  return (
    <Autocomplete
      multiple
      options={tags ?? []}
      getOptionLabel={(option: WorkTag) => option.name}
      defaultValue={[]}
      filterSelectedOptions
      renderInput={(params) => (
        <TextField
          {...params}
          label="タグ"
          placeholder="タグ名を入力"
        />
      )}
      onChange={props.onChange}
    />
  );
};

export default TagSelectBox;
