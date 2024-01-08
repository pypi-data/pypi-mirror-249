.. |br| raw:: html

   <br />

.. _timedelta: https://docs.python.org/3.8/library/datetime.html#timedelta-objects

=====
Usage
=====

To use Stilpy in a project:

>>> from stilpy import TimeGaps 

Minimal example
-----------------

Suppose that you have serveral records of time stored in a list of dictionaries, like this:
:

>>> list_dict = [
...         {'t_dt':'start','dt': '2019-12-19 10:00:00'},
...         {'t_dt':'end', 'dt': '2019-12-19 13:30:20'},
...         {'t_dt':'start', 'dt': '2019-12-19 14:30:00'},
...         {'t_dt':'start', 'dt': '2019-12-19 15:30:00'},
...         {'t_dt':'end', 'dt': '2019-12-19 17:00:35'},
...         {'t_dt':'start', 'dt': '2019-12-19 09:00:00'}
...         ]

As you can see, these are time intervals. They have a start and an end point, but
they are not in the rigth order. The first two elements are correct. But then we 
have two start points together. And the last one is a start point record that
should be on the top of the list because is older than te others.
What Stilpy can do for us is to make an iterator with those records, matching the
start points with the right end, or giving them an unknown end if they don't have
one of their own.

To do that we need to make an instance of the 
`TimeGaps <API.html#module-stilpy.timegaps>`__ class.

``TimeGaps`` recieves several parameters. Some of them are optionals. Let's see
which ones are needed for our example:

    **iterable:** 
        An iterable object that contains a list of items.
        Those items must be dicts or dictlike objects. Lists,
        tuples and objects with ``__dict__`` atribute are accepted as
        well. |br| Every item, must content in itself the next items: |br| 
        1. A ``datetime`` object or a string format ``datetime``. In our
        case, we have the second option. |br|
        2. An item that defines if the first element that we just mentioned
        is an initial or a final time point of a time interval.

    **tag_loc:** 
        It tells ``TimeGaps`` where to find the tag that tells if the
        item is a start point or an end.

    **i_tag:**
        The name of the initial time tag in the iterable. Default is ``'start'``.

    **f_tag:** 
        The name of the final time tag in the iterable. Default is ``'end'``.

    **dt_loc:**
        The location, inside each element of the iterable, of the
        ``datetime`` information. It can be a dictionary key or an index,
        depending on the collection.

The rest of parameters are optionals, and we won't need them yet.

Now we can call create the ``TimeGaps`` object, passing the arguments in 
order:

>>> ti = TimeGaps(list_dict, 't_dt', 'start', 'end', 'dt')

Now we have our iterator. Every item is a ``TimeInterval`` object with
some attributes like `start <API.html#stilpy.timeinterval.TimeInterval.start>`__,
`end <API.html#stilpy.timeinterval.TimeInterval.end>`__,
`duration <API.html#stilpy.timeinterval.TimeInterval.duration>`__ and 
`is_perfect <API.html#stilpy.timeinterval.TimeInterval.is_perfect>`__.
You can add any other attribute to the 
`TimeInterval object <API.html#module-stilpy.timeinterval>`__, but we will see
that later. Now we are just going to print each element. But first, we will ask
for the sum of the durations of all its intervals. At the same time, we'll pass
an argument that will be returned if ``TimeGaps`` is unable to make the sum 
because some interval hasn't a duration. By default ``None`` will be returned.

>>> ti.total_duration('Sorry! Some interval is not perfect')
'Sorry! Some interval is not perfect'
>>> for i, t in enumerate(ti):
...     s = t.start if t.start!='' else 'unknown'
...     e = t.end if t.end!='' else 'unknown'
...     d = t.duration if t.duration!='' else 'unknown'
...     print(f'Interval {i + 1} ->')
...     print(f'\t\tStart: {s}')
...     print(f'\t\tEnd: {e}')
...     print(f'\t\tDuration: {d}')
Interval 1 ->
                Start: 2019-12-19 09:00:00
                End: unknown
                Duration: unknown
Interval 2 ->
                Start: 2019-12-19 10:00:00
                End: 2019-12-19 13:30:20
                Duration: 3:30:20
Interval 3 ->
                Start: 2019-12-19 14:30:00
                End: unknown
                Duration: unknown
Interval 4 ->
                Start: 2019-12-19 15:30:00
                End: 2019-12-19 17:00:35
                Duration: 1:30:35

You can see that, by default, an empty property is set to ``''``.

If we pass a perfect time intervals collection
`total_duration <API.html#stilpy.timegaps.TimeGaps.total_duration>`__
will return a very different result. Let's see an example.

>>> perfect_list_dict = [
...         {'t_dt':'start','dt': '2019-12-19 10:00:00'},
...         {'t_dt':'end', 'dt': '2019-12-19 13:30:20'},
...         {'t_dt':'start', 'dt': '2019-12-19 14:30:00'},
...         {'t_dt':'end', 'dt': '2019-12-19 17:00:35'},
...         ]
>>> ti_p = TimeGaps(perfect_list_dict, 't_dt', 'start', 'end', 'dt')
>>> for t in ti_p:
...     print(t.duration)
3:30:20
2:30:35
>>> ti_p.total_duration()
datetime.timedelta(seconds=21655)
>>> print(ti_p.total_duration())
6:00:55

As you can see, this method returns a timedelta_ object with the sum
of the duration of every ``TimeInterval``.

Time intervals with groups
--------------------------

In the previous example, we just got the records that need to be ordered
and put together. But what happens if we have records that belong to
different groups, all together in the same collection? Well, for that we
have the ``group_by`` parameter.

Let's try another example.

Imagine we're working with the sign-in and sign-out of the employees from the 
company's web application. We should have something like this:

>>> keys_dicts = [
...     {
...         'name': 'Eve', 'surname': 'Palmer',
...         't_dt':'start', 'dt': '2019-12-19 10:00:00'
...     },
...     {
...         'name': 'Cecilia', 'surname': 'Park',
...         't_dt':'end', 'dt': '2019-12-19 11:00:05'
...     },
...     {
...         'name': 'Moses', 'surname': 'Farrel',
...         't_dt':'start', 'dt': '2019-12-19 10:00:05'
...     },
...     {
...         'name': 'Eve', 'surname': 'Palmer',
...         't_dt':'end', 'dt': '2019-12-19 13:30:20'
...     },
...     {
...         'name': 'Moses', 'surname': 'Farrel',
...         't_dt':'end', 'dt': '2019-12-19 13:45:15'
...     },
...     {
...         'name': 'Eve', 'surname': 'Palmer',
...         't_dt':'start', 'dt': '2019-12-19 14:30:00'
...     },
...     {
...         'name': 'Cecilia', 'surname': 'Park',
...         't_dt':'start', 'dt': '2019-12-19 15:30:00'
...     },
...     {
...         'name': 'Cecilia', 'surname': 'Park',
...         't_dt':'end', 'dt': '2019-12-19 17:00:35'
...     },
...     {
...         'name': 'Moses', 'surname': 'Farrel',
...         't_dt':'start', 'dt': '2019-12-19 09:00:00'
...     },
...     {
...         'name': 'Cecilia', 'surname': 'Park',
...         't_dt':'start', 'dt': '2019-12-19 10:00:02'
...     },
... ]

We cannot order these records based only on their temporary value.
If we do that, we'll be ignoring that every record belongs to a different person.
So we have to use the ``group_by`` parameter by saying which keys should use
`TimeGaps <API.html#module-stilpy.timegaps>`__ to order this records. Let's see how:

For our example we need to group the records by name and surname. ``group_by``
is a keyword argumen and it's expecting a single element or a collection,
preferred a tuple. So we do it like this:

>>> ti_g = TimeGaps(
...                     keys_dicts, 't_dt', 'start', 'end', 'dt',
...                     group_by=('name', 'surname')
...        )

But, additionally maybe we want to store that pairs of keys and values 
of names and surnames inside of te ``TimeInterval`` objects, in order 
to differentiate some intervals from others. As we said before ``group_by`` 
is a keyword argumen. Any other positional argumen used to instanciate the 
`TimeGaps <API.html#module-stilpy.timegaps>`__ class different of 
``iterable``, ``tag_loc``, ``i_tag``, ``f_tag``
and ``dt_loc`` will be treated as the key for creating the additional
attributes for the ``TimeInterval`` objects of a ``TimeGaps`` iterator (this
option is not aviable if your are working with an iterable of any collection
that works with index instead of keys, like list, tuples... So if you have a
list of list or a list of tuple, your can use ``group_by`` but you can't add
additionals attributes to the ``TimeInterval`` objects). So we can change the
instanciation like this:

>>> ti_g = TimeGaps(
...                     keys_dicts, 't_dt', 'start', 'end', 'dt',
...                     'name', 'surname',
...                     group_by=('name', 'surname')
...        )

Now if we print every element we should see how the ``TimeInterval`` objects 
has been created by groups, and how they are ordered in the collection.

>>> for i, tg in enumerate(ti_g):
...     s = tg.start if tg.start!='' else 'unknown'
...     e = tg.end if tg.end!='' else 'unknown'
...     d = tg.duration if tg.duration!='' else 'unknown'
...     emp = f'{tg.name} {tg.surname}'
...     print(f'Interval {i + 1} ->')
...     print(f'\t\tEmployee: {emp}')
...     print(f'\t\tStart: {s}')
...     print(f'\t\tEnd: {e}')
...     print(f'\t\tDuration: {d}')
Interval 1 ->
                Employee: Moses Farrel
                Start: 2019-12-19 09:00:00
                End: unknown
                Duration: unknown
Interval 2 ->
                Employee: Eve Palmer
                Start: 2019-12-19 10:00:00
                End: 2019-12-19 13:30:20
                Duration: 3:30:20
Interval 3 ->
                Employee: Cecilia Park
                Start: 2019-12-19 10:00:02
                End: 2019-12-19 11:00:05
                Duration: 1:00:03
Interval 4 ->
                Employee: Moses Farrel
                Start: 2019-12-19 10:00:05
                End: 2019-12-19 13:45:15
                Duration: 3:45:10
Interval 5 ->
                Employee: Eve Palmer
                Start: 2019-12-19 14:30:00
                End: unknown
                Duration: unknown
Interval 6 ->
                Employee: Cecilia Park
                Start: 2019-12-19 15:30:00
                End: 2019-12-19 17:00:35
                Duration: 1:30:35

If we have two records that will be conform an interval add an extra
argument this will be the expected behaviour:

* if the key is present in both records with the same value, that value
  will be used to populate the new attribute
* if the key is present in both records with different values, the 
  attribute will be populated with a tuple whose first element is the
  value the start record's value for that key, and the second will be 
  the end record's value for that key
* if the key is present just in one of the records, its value will be 
  used to populate the attribute

But what happens if we want different iterators, one per element of the group?
Let’s say that we want a iterator for every employee. You can easily have it. In 
fact you will get a list of ``TimeGaps`` objects, one for each employee. You
just need to call the
`grouped_intervals <API.html#stilpy.timegaps.TimeGaps.grouped_intervals>`__ property.

First let's see the groups that we have, by calling the
`grouper_tags <API.html#stilpy.timegaps.TimeGaps.grouper_tags>`__ property.

>>> for gt in ti_g.grouper_tags:
...     print(gt)
{'name': 'Cecilia', 'surname': 'Park'}
{'name': 'Eve', 'surname': 'Palmer'}
{'name': 'Moses', 'surname': 'Farrel'}

Now let's get a list of ``TimeGaps``, one per employee and see what it has
inside.

>>> grouped_ti = ti_g.grouped_intervals
>>> for group in grouped_ti:
...     print('Group number:', grouped_ti.index(group) + 1)
...     print('Total duration:', group.total_duration('unable'))
...     for i, tg in enumerate(group):
...             s = tg.start if tg.start!='' else 'unknown'
...             e = tg.end if tg.end!='' else 'unknown'
...             d = tg.duration if tg.duration!='' else 'unknown'
...             emp = f'{tg.name} {tg.surname}'
...             print(f'Interval {i + 1} ->')
...             print(f'\t\tEmployee: {emp}')
...             print(f'\t\tStart: {s}')
...             print(f'\t\tEnd: {e}')
...             print(f'\t\tDuration: {d}')
Group number: 1
Total duration: 2:30:38
Interval 1 ->
                Employee: Cecilia Park
                Start: 2019-12-19 10:00:02
                End: 2019-12-19 11:00:05
                Duration: 1:00:03
Interval 2 ->
                Employee: Cecilia Park
                Start: 2019-12-19 15:30:00
                End: 2019-12-19 17:00:35
                Duration: 1:30:35
Group number: 2
Total duration: unable
Interval 1 ->
                Employee: Eve Palmer
                Start: 2019-12-19 10:00:00
                End: 2019-12-19 13:30:20
                Duration: 3:30:20
Interval 2 ->
                Employee: Eve Palmer
                Start: 2019-12-19 14:30:00
                End: unknown
                Duration: unknown
Group number: 3
Total duration: unable
Interval 1 ->
                Employee: Moses Farrel
                Start: 2019-12-19 09:00:00
                End: unknown
                Duration: unknown
Interval 2 ->
                Employee: Moses Farrel
                Start: 2019-12-19 10:00:05
                End: 2019-12-19 13:45:15
                Duration: 3:45:10

You can easily see that a ``TimeGaps`` iterator has been created for each 
employee with the same methods and properties as their ``TimeGaps`` object's
father. And that's why we could call the 
`total_duration <API.html#stilpy.timegaps.TimeGaps.total_duration>`__ method 
for each ``group`` in ``grouped_ti`` collection.

Total duration anyway
---------------------

But what happens if you want to display the the duration of a group, even if it's
not perfect? Maybe you just want to dispaly it differently. Well, in those 
cases you can use the 
`total_duration_anyway <API.html#stilpy.timegaps.TimeGaps.total_duration_anyway>`__ 
method.

Let's rework the previous example adding this new functionality.

>>> grouped_ti = ti_g.grouped_intervals
>>> # Example with total_duration_anyway() method
... for group in grouped_ti:
...     print('Group number:', grouped_ti.index(group) + 1)
...     # If there is a perfect duration it will be printed
...     if (tot_duration := group.total_duration(False)) != False:
...             print('Total duration:', tot_duration)
...     # Otherwise, the imperfect duration will be displayed
...     else:
...             print('Not perfect duration ', group.total_duration_anyway())
...     for i, tg in enumerate(group):
...             s = tg.start if tg.start!='' else 'unknown'
...             e = tg.end if tg.end!='' else 'unknown'
...             d = tg.duration if tg.duration!='' else 'unknown'
...             emp = f'{tg.name} {tg.surname}'
...             print(f'Interval {i + 1} ->')
...             print(f'\t\tEmployee: {emp}')
...             print(f'\t\tStart: {s}')
...             print(f'\t\tEnd: {e}')
...             print(f'\t\tDuration: {d}')
...
Group number: 1
Total duration: 2:30:38
Interval 1 ->
                Employee: Cecilia Park
                Start: 2019-12-19 10:00:02
                End: 2019-12-19 11:00:05
                Duration: 1:00:03
Interval 2 ->
                Employee: Cecilia Park
                Start: 2019-12-19 15:30:00
                End: 2019-12-19 17:00:35
                Duration: 1:30:35
Group number: 2
Not perfect duration  3:30:20
Interval 1 ->
                Employee: Eve Palmer
                Start: 2019-12-19 10:00:00
                End: 2019-12-19 13:30:20
                Duration: 3:30:20
Interval 2 ->
                Employee: Eve Palmer
                Start: 2019-12-19 14:30:00
                End: unknown
                Duration: unknown
Group number: 3
Not perfect duration  3:45:10
Interval 1 ->
                Employee: Moses Farrel
                Start: 2019-12-19 09:00:00
                End: unknown
                Duration: unknown
Interval 2 ->
                Employee: Moses Farrel
                Start: 2019-12-19 10:00:05
                End: 2019-12-19 13:45:15
                Duration: 3:45:10

As you can see above, groups 1 and 3 have a perfect duration, and this is displayed 
with the label 'Duration:'. On the other hand, group number 2 has an interval 
without a valid duration (``unknown``), so Stilpy takes the remaining valid 
durations, and returns a partial duration, used by our program to display the 
result, labeled as 'Duration not perfect'.