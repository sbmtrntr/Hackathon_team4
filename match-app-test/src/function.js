const formatData = ({data}) => {
  const keys = data.values[0];
  const _data = data.values.slice(1);
  const obj = _data.map(arr => Object.assign({}, ...keys.map((k, i) => ({ [k]: arr[i] }))));
  return obj
}