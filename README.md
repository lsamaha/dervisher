# dervisher

Demonstrates use of AWS kinesis and dynamodb for application events.

## About

Dervisher is a Python 3 package used to how applications should post events to kinesis for storage and evaluation by
the chain of event consumers defined in the dervish GitHub project.

## Getting Started

A dervisher is created by installing the dervisher python package and calling the entry point whirl and providing a
numeric rotation per minute argument.

## Example

```bash
pip install dervisher
dervish
usage: dervisher rpm
```

## Result

The result of invoking the dervisher is:
- validation of the associated AWS account for this environment (see AWS' own environment documentation)
- creation of a kinesis stream in the default region called "dervisher" (if it doesn't already exist)
- generation of a stream of application events at the specified rate as the dervisher whirls back and forth

## Example Output
```bash
dervish 20
finding stream dervish
a dervisher starts whirling at 20 rpm
posting {"env": "dev", "event_class": "start", "event_type": "service", "pretty": false, "product": "mimi", "subtype": "whirl"}
posting {"env": "dev", "event_class": "start", "event_type": "whirl", "pretty": false, "product": "mimi", "subtype": "back"}
posting {"env": "dev", "event_class": "complete", "event_type": "whirl", "pretty": false, "product": "mimi", "subtype": "back"}
posting {"env": "dev", "event_class": "start", "event_type": "whirl", "pretty": false, "product": "mimi", "subtype": "forth"}
posting {"env": "dev", "event_class": "complete", "event_type": "whirl", "pretty": false, "product": "mimi", "subtype": "forth"}
posting {"env": "dev", "event_class": "stop", "event_type": "service", "pretty": false, "product": "mimi", "subtype": "whirl"}
```

## Do It Yourself

By reviewing the docs and the whirling class, it should be easy to see how to generate new streams with new app events.

```python
dervisher = Dervisher(product = 'mimi', post=Post(stream=Stream(KinesisConnection())))
dervisher.post.event(Event(event_class='start', event_type='whirl', subtype='forth', env='dev', product=self.product))
```
