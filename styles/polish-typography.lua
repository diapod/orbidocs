local quote_levels = {
  { "„", "”" },
  { "«", "»" },
  { "‚", "’" },
}

local function quoted_markers(depth, quote_type)
  if tostring(quote_type) ~= "DoubleQuote" then
    return "‚", "’"
  end

  local level = quote_levels[depth] or quote_levels[#quote_levels]
  return level[1], level[2]
end

local function transform_inlines(inlines, depth)
  local result = pandoc.List()

  for _, inline in ipairs(inlines) do
    if inline.t == "Quoted" then
      local open_mark, close_mark = quoted_markers(depth, inline.quotetype)
      result:insert(pandoc.Str(open_mark))

      local nested = transform_inlines(inline.content, depth + 1)
      for _, item in ipairs(nested) do
        result:insert(item)
      end

      result:insert(pandoc.Str(close_mark))
    else
      if inline.content then
        inline.content = transform_inlines(inline.content, depth)
      end

      result:insert(inline)
    end
  end

  return result
end

function Quoted(el)
  local open_mark, close_mark = quoted_markers(1, el.quotetype)
  local inlines = { pandoc.Str(open_mark) }

  for _, inline in ipairs(transform_inlines(el.content, 2)) do
    table.insert(inlines, inline)
  end

  table.insert(inlines, pandoc.Str(close_mark))

  return inlines
end
