# tpify
_Pronounced like "[typify](https://www.dictionary.com/browse/typify)"_

Return, don't raise.

## What this does
**tpify** allows you to configure functions to return contextual statuses, and to return errors rather than raise them.

## Why?
Python programs often have inconsistent conventions when it comes to returning data. They also have a problem of not making it clear when exceptions can be raised. This is an attempt to see if there is enough benefit to violate Pythonic conventions to get some additional reliability and improved (albeit verbose, [Go-like](https://go.dev/blog/error-handling-and-go)) error handling.

## Benefits
### No more `try`/`except`
All tpified functions return an object, removing the need to wrap functions in a `try` block. This leads to safer, more predictable execution paths. Exceptions are still returned when raised, and the ability to customize which status code is returned means the type and source of error can be more easily communicated.

### Better context
`TPResponse` objects contain status codes, enabling richer context about successes and failures. For example:
* Functions that return `True` can return context about whether a new resource was created using `tp.Created` status, or updated using the `tp.Updated` status.
* Functions that return `None` can return information about whether `None` means a successful or failed execution.
* Failure origination can be returned to indicate if the error is an error with the input data (`tp.InputError` responses), or with the processing of the data iteself (`tp.ProcessingError` responses).
If you can't find a code that works for you, there is always the option to create your own.

## Dos and Don'ts
**DO: Check your `TPResponse` status codes**. While you _can_ just take the `content` of a `TPResponse` if you only want the safety of avoiding unintended `raise` statements, it is encouraged to have some paradigm to process `status_code` values.

**DO: append `_tp` at the end of tpified function names**. This communicates that this function returns a `TPResponse` object, since the function itself may show it returns a different type.
  ```python
  from tpify import tpify

  @tpify()
  def fibonacci_tp(n: int) -> int:
    # TODO: Implement fibonacci recursively
  ```
**DO: use `@tpify()` after non-return type-modifying decorators**. If you have multiple decorators on a tpified function, have `tpify()` be after those that don't modify return types, so that the return types are accounted for in any other decorator logic.
  ```python
  from functools import cache
  from tpify import tpify

  @cache
  @tpify()
  def fibonacci_tp(n: int):
    # TODO: Implement fibonacci recursively
  ```

## Advanced uses
### `exception_type_map`
The `@tpify()` decorator takes an optional argument that maps raised exceptions to `TPStatus` codes. This allows you to map errors to status codes other than the default `TPStatus.ProcessingError` value. For example:

  ```python
  import json
  from typing import Any

  from tpify import append_statuses_tp, tp, tpify


  @tpify(exception_type_map={json.JSONDecodeError: tp.InputError})
  def parse_json_tp(json_str: str) -> Any:
      return (tp.OK, json.loads(json_str))


  if __name__ == "__main__":
      status, resp = parse_json_tp('{"fibNum": 13}')
      print(type(status))
      print(status == tp.OK)
      print(status == tp["OK"])
      print(resp)

      status, resp = parse_json_tp('{"fibNum": error}')
      print(type(status))
      print(status == tp.InputError)
      print(status == tp["InputError"])
      print(resp)
  ```
  > <enum 'TPStatus'><br>
True<br>
True<br>
{'fibNum': 13}<br>
<enum 'TPStatus'><br>
True<br>
True

### Adding custom `TPStatus` values
You can add custom `TPStatus` values using `append_statuses_tp()`. This ends up creating a new `TPStatusCustom` object that contains the original `TPStatus` codes, as well as the new ones you request. Here's the gist of how that works:
  ```python
  import json
  from typing import Any

  from tpify import append_statuses_tp, tp, tpify

  tp_status, tp_cust = append_statuses_tp(
      statuses=(
          "JSONParseOK",
          "JSONParseFailed",
      )
  )
  if tp_status != tp.OK:
      print(f"ERROR: Could not create new statuses: {tp_cust}")
      exit(1)


  @tpify(exception_type_map={json.JSONDecodeError: tp_cust.JSONParseFailed})
  def parse_json_tp(json_str: str) -> Any:
      return (tp_cust.JSONParseOK, json.loads(json_str))


  if __name__ == "__main__":
      status, resp = parse_json_tp('{"fibNum": 13}')
      print(type(status))
      print(status == tp_cust.JSONParseOK)
      print(status == tp_cust["JSONParseOK"])
      print(resp)

      status, resp = parse_json_tp('{"fibNum": error}')
      print(type(status))
      print(status == tp_cust.JSONParseFailed)
      print(status == tp_cust["JSONParseFailed"])
      print(resp)
  ```
  > <enum 'TPStatusCustom'><br>
True<br>
True<br>
{'fibNum': 13}<br>
<enum 'TPStatusCustom'><br>
True<br>
True<br>
Expecting value: line 1 column 12 (char 11)