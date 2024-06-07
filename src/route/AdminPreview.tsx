import AMISRenderer from "@/component/AMISRenderer";
import React, {useEffect, useState} from "react";
import {API_HOST} from "@/config";

export default function AdminPreview(props: { schemaApi: string }) {
  let {schemaApi} = props;
  let [schema, setSchema] = useState({});
  useEffect(() => {
    (async () => {
      console.log("schemaApi is ", schemaApi)
      let url = `${API_HOST}${schemaApi}`
      let schema = await fetch(url).then(res => res.json());
      setSchema(schema);
    })();
  }, []);

  return (
    <AMISRenderer schema={schema}/>
  )
}
